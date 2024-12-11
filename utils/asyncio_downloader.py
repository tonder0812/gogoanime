import itertools
import math
import re
import subprocess
import threading
import time
from mmap import mmap
from pathlib import Path
from threading import Thread
import traceback
from typing import AsyncIterator, Awaitable, Callable, Iterable, Protocol
from urllib.parse import urlparse

import anyio
import httpx

from printer import AbstractPrinter
from utils.debugging import debug_log
from utils.format import delta_time_str, new_random_file
from utils.prediction import Prediction


def tries_iterator(tries: int) -> Iterable[int]:
    if tries < 0:
        return itertools.count()
    else:
        return range(tries)


async def get_download_size(
    client: httpx.AsyncClient, url: str, tries: int
) -> int | None:
    for _ in tries_iterator(tries):
        try:
            head = await client.head(url)
            head.raise_for_status()
            total = head.headers.get("Content-Length")
            if total is None:
                return -1
            try:
                return int(total)
            except ValueError:
                return -1
        except anyio.EndOfStream:
            pass
        except httpx.TimeoutException:
            pass
        except httpx.NetworkError:
            pass
        except httpx.ProtocolError:
            pass
        except httpx.TooManyRedirects:
            pass


async def get_suports_range(client: httpx.AsyncClient, url: str, tries: int) -> bool:
    for _ in tries_iterator(tries):
        try:
            head = await client.head(url, headers={"range": "bytes=0-100"})
            head.raise_for_status()
            if head.status_code != 206:
                return False
            range_header = head.headers.get("Content-Range")
            if range_header is None:
                return False
            return range_header.startswith("bytes 0-100")
        except anyio.EndOfStream:
            pass
        except httpx.TimeoutException:
            pass
        except httpx.NetworkError:
            pass
        except httpx.ProtocolError:
            pass
        except httpx.TooManyRedirects:
            pass
    return False


async def empty_stream(_: int, __: int) -> AsyncIterator[bytes | None]:
    return
    yield


ContentType = AsyncIterator[bytes | None]
ContentGeneratorType = Callable[[int, int], ContentType]
ContentGeneratorTypeNoSize = Callable[[], ContentType]
SrcType = tuple[int | None, bool, ContentGeneratorType]
M3U8SrcType = tuple[list[Path] | None, list[int], str, list[ContentGeneratorTypeNoSize]]


# SrcGeneratorType = Callable[[int, int], Awaitable[SrcType]]
class SrcGeneratorType(Protocol):

    def __call__(
        self, tries: int, force_unsegmented: bool = False, /
    ) -> Awaitable[SrcType]: ...


class M3U8SrcGeneratorType(Protocol):

    def __call__(self, tries: int, /) -> Awaitable[M3U8SrcType]: ...


def httpx_ranged_builder(
    url: str,
    headers: dict[str, str] | None = None,
    client: httpx.AsyncClient | None = None,
) -> SrcGeneratorType:
    if client is None:
        client = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=None, max_keepalive_connections=None),
            follow_redirects=True,
        )
    if headers:
        client.headers = headers

    async def src(tries: int, force_unsegmented: bool = False) -> SrcType:
        size = None

        try:
            size = await get_download_size(client, url, tries)
        except Exception:
            debug_log("========================================================", 1)
            debug_log(f"Error getting download size for: {url}", 1)
            debug_log(f"", 1)
            debug_log(traceback.format_exc(), 1)
        if size is None:
            return None, False, empty_stream

        supports_range = False
        if not force_unsegmented and size > 5 * 1024 * 1024:
            try:
                supports_range = await get_suports_range(client, url, tries)
            except Exception:
                debug_log("========================================================", 1)
                debug_log(f"Error checking if server supports range for: {url}", 1)
                debug_log(f"", 1)
                debug_log(traceback.format_exc(), 1)

        async def stream(start: int, end: int):
            try:
                async with client.stream(
                    "GET",
                    url,
                    headers=(
                        {"range": f"bytes={start}-{end-1}"} if supports_range else {}
                    ),
                    timeout=60,
                ) as r:
                    if supports_range:
                        if r.status_code != 206:
                            raise HTTPStatusCodeNot206(
                                r.status_code, url, f"{start}-{end-1}", r.headers
                            )
                        if not r.headers["Content-Range"].startswith(
                            f"bytes {start}-{end-1}"
                        ):
                            raise InvalidHTTPRange(url, f"{start}-{end-1}", r.headers)
                    async for chunk in r.aiter_bytes(1024):
                        if chunk:
                            yield chunk
            except anyio.EndOfStream:
                yield None
            except httpx.TimeoutException:
                yield None
            except httpx.NetworkError:
                yield None
            except httpx.ProtocolError:
                yield None

        return size, supports_range, stream

    return src


class HTTPStatusCodeNot206(Exception):
    def __init__(
        self, status_code: int, url: str, range: str, headers: httpx.Headers
    ) -> None:
        super().__init__(
            f"Invalid HTTP response to range request:\n  status code: {status_code}\n  url: {url}\n  range: {range}\n  response headers: {headers}"
        )


class InvalidHTTPRange(Exception):
    def __init__(self, url: str, range: str, headers: httpx.Headers) -> None:
        super().__init__(
            f"Range missmatch between request and response:\n  url: {url}\n  requested range: {range}\n  response range: {headers["Content-Range"]}\n  response headers: {headers}"
        )


def calculate_ranges(size: int, segments: int):
    splits: list[int] = []
    remainder = size % segments
    integer = size // segments
    for i in range(segments):
        splits.append(integer)
    for i in range(remainder):
        splits[i] += 1
    ranges: list[int] = [0]
    for i in range(segments):
        ranges.append(ranges[-1] + splits[i])
    return ranges


# Based on https://codereview.stackexchange.com/questions/265814/python-multi-connection-downloader
class DownloadTask:
    sem = threading.Semaphore()

    @classmethod
    def set_max_concurrent_downloads(cls, concurrent_downloads: int):
        cls.sem = threading.Semaphore(concurrent_downloads)

    def __init__(
        self,
        *,
        src: SrcGeneratorType,
        filename: Path,
        printr: AbstractPrinter,
        download_id: str,
        segments: int = 10,
    ) -> None:
        self.src = src
        self.printr = printr
        self.download_id = download_id

        self.mm = None
        self.file = None
        self.filename = filename

        self.size = 0
        self.received = 0
        self.start_time = 0
        self.last_status_update = 0
        self.estimate: Prediction | None = None
        self.estimate_thread: Thread | None = None

        self.segments = segments
        self.completed = []
        self.supports_range = False
        self.ranges: list[int] = []

        self.content: ContentGeneratorType | None = None
        self.adquired_semaphore = False

    async def setup(self, tries: int):
        self.received = 0

        if self.start_time == 0:
            self.start_time = time.time()

        size, self.supports_range, self.content = await self.src(
            tries, self.segments == 1
        )
        if size is None:
            return False

        self.size = size
        self.printr.set(self.download_id + "_max", self.size)
        self.printr.set(self.download_id + "_perc", 0)

        if not self.supports_range:
            self.segments = 1

        self.filename.touch()

        self.adquired_semaphore = True
        self.sem.acquire()
        if self.size > 0:
            self.file = self.filename.open(mode="r+b")
            self.file.truncate(self.size)
            self.mm = mmap(self.file.fileno(), self.size)
        else:
            self.file = self.filename.open(mode="wb")

        self.segment_size = 0
        while self.segments > 1:
            self.segment_size = self.size / self.segments
            if self.segment_size > 1024:
                break
            self.segments -= 1

        self.ranges = calculate_ranges(self.size, self.segments)

        debug_log("========================================================")
        debug_log(f"[{self.download_id}] info")
        debug_log(f"file: {self.filename}")
        debug_log(f"supports range: {self.supports_range}")
        if self.supports_range:
            debug_log(f"segments: {self.segments}")
            debug_log(f"segment size: {self.segment_size}")
            debug_log(f"segment stops: {self.ranges}")

        self.completed = [False for _ in range(self.segments)]

        if self.size > 0:
            self.estimate = Prediction(self.printr, self.download_id, self.size)
            self.estimate_thread = Thread(target=self.estimate.run)
            self.estimate_thread.start()

        return True

    def stop(self):
        if self.estimate is not None and self.estimate_thread is not None:
            self.estimate.stop()
            self.estimate_thread.join()
        self.update_status(True)
        if self.mm is not None:
            self.mm.close()
        if self.file is not None:
            self.file.close()
        if self.adquired_semaphore:
            self.sem.release()

    async def multidown(self, tries: int, index: int) -> bool:
        assert self.content is not None
        assert self.file is not None

        count = 0
        start = self.ranges[index]
        end = self.ranges[index + 1]

        for _ in tries_iterator(tries):
            try:
                if not self.supports_range:
                    count = 0

                i = start + count
                async for chunk in self.content(start + count, end):
                    if chunk is None:
                        break

                    if self.estimate:
                        self.estimate.add(len(chunk))

                    if self.mm is None:
                        self.file.write(chunk)
                    else:
                        self.mm[i : i + len(chunk)] = chunk

                    count += len(chunk)
                    self.received += len(chunk)
                    i += len(chunk)

                    self.update_status()

                if count == (end - start):
                    self.completed[index] = True
                    return True
            except Exception:
                debug_log("========================================================", 1)
                debug_log(
                    f"[{self.download_id}] Error while downloading segment {index} ({start}-{end})",
                    1,
                )
                debug_log(f"", 1)
                debug_log(traceback.format_exc(), 1)
            self.received -= count

        return False

    def update_status(self, force: bool = False):
        current = time.time()
        if (current - self.last_status_update) > 0.1 or force:
            self.last_status_update = current
            with self.printr.get_lock():
                self.printr.set(self.download_id + "_progress", self.received)
                if self.estimate:
                    self.printr.set(
                        self.download_id + "_perc", (100 * self.received) / self.size
                    )
                else:
                    self.printr.set(self.download_id + "_perc", math.nan)
                self.printr.set(
                    self.download_id + "_timer",
                    delta_time_str(self.start_time, current),
                )


ffmpeg_lock = threading.Lock()


def downloader_func(
    c: httpx.AsyncClient, link: str, expected_size: int
) -> ContentGeneratorTypeNoSize:

    async def download() -> AsyncIterator[bytes | None]:
        async with c.stream(
            "GET",
            link,
            headers={
                "Accept-Language": "en-GB,en;q=0.5",
            },
        ) as r:
            if not r.headers["Content-Length"].startswith(f"{expected_size}"):
                raise Exception("")
            async for chunk in r.aiter_bytes(1024):
                if chunk:
                    yield chunk

    return download


def M3U8_builder(
    c: httpx.AsyncClient, link: str, dest_folder: Path
) -> M3U8SrcGeneratorType:

    # print(matches)
    async def src(tries: int) -> M3U8SrcType:
        r = await c.get(
            link,
            headers={
                "Accept-Language": "en-GB,en;q=0.5",
            },
        )
        # print(r.content)
        m3u8_content = r.content.decode()
        matches: list[tuple[str, str]] = re.findall('(https://.*?)("|\n)', m3u8_content)

        tmps: list[Path] = []
        sizes: list[int] = []
        downloader_functions: list[ContentGeneratorTypeNoSize] = []
        for match, _ in matches:
            path = Path(urlparse(match).path)
            extension = path.suffix
            tmp_file = new_random_file(dest_folder, extension)
            size = await get_download_size(c, match, tries)
            if size is None:
                return None, [], "", []
            downloader_functions.append(downloader_func(c, match, size))
            sizes.append(size)
            tmps.append(tmp_file)
            m3u8_content = m3u8_content.replace(match, str(tmp_file).replace("\\", "/"))
        return (tmps, sizes, m3u8_content, downloader_functions)

    return src


class M3U8DownloadTask:
    sem = threading.Semaphore()

    @classmethod
    def set_max_concurrent_downloads(cls, concurrent_downloads: int):
        cls.sem = threading.Semaphore(concurrent_downloads)

    def __init__(
        self,
        *,
        src: M3U8SrcGeneratorType,
        filename: Path,
        printr: AbstractPrinter,
        download_id: str,
    ) -> None:
        self.src = src
        self.printr = printr
        self.download_id = download_id

        self.files: list[Path] = []
        self.sizes: list[int] = []
        self.size = 0
        self.filename = filename
        self.m3u8_file = filename.with_suffix(".m3u8")

        self.segments = 0
        self.received = 0
        self.start_time = 0
        self.last_status_update = 0
        self.estimate: Prediction | None = None
        self.estimate_thread: Thread | None = None

        self.completed = []

        self.content: list[ContentGeneratorTypeNoSize] | None = None
        self.adquired_semaphore = False

    async def setup(self, tries: int):
        if self.start_time == 0:
            self.start_time = time.time()

        files, self.sizes, m3u8_content, self.content = await self.src(tries)
        if files is None:
            return False

        assert len(files) == len(self.sizes) and len(files) == len(self.content)

        self.m3u8_file.write_text(m3u8_content)
        self.files = files
        self.segments = len(self.files)
        self.size = sum(self.sizes)
        self.printr.set(self.download_id + "_max", self.size)
        self.printr.set(self.download_id + "_perc", 0)

        self.adquired_semaphore = True

        debug_log("========================================================")
        debug_log(f"[{self.download_id}] info")
        debug_log(f"file: {self.filename}")
        debug_log(f"segments: {self.segments}")

        self.completed = [False for _ in range(self.segments)]

        self.estimate = Prediction(self.printr, self.download_id, self.size)
        self.estimate_thread = Thread(target=self.estimate.run)
        self.estimate_thread.start()

        return True

    def stop(self):
        if self.estimate is not None and self.estimate_thread is not None:
            self.estimate.stop()
            self.estimate_thread.join()

        self.update_status(True)

        with ffmpeg_lock:
            with (self.filename.parent / "debug.log").open("a") as f:
                self.printr.set(self.download_id + "_try", "processing")

                subprocess.run(
                    [
                        "ffmpeg",
                        "-allowed_extensions",
                        "ALL",
                        "-i",
                        self.m3u8_file.absolute(),
                        "-codec",
                        "copy",
                        "-bsf:a",
                        "aac_adtstoasc",
                        "-y",
                        self.filename,
                    ],
                    stdout=f,
                    stderr=f,
                )
                #  [
                #     "ffmpeg",
                #     "-allowed_extensions",
                #     "ALL",
                #     "-i",
                #     self.m3u8_file.absolute(),
                #     "-vcodec",
                #     "h264",
                #     "-b:v",
                #     "1000k",
                #     "-acodec",
                #     "mp3",
                #     "-y",
                #     self.filename,
                # ],
                self.printr.set(self.download_id + "_try", "processed")

            for file in self.files:
                file.unlink(missing_ok=True)
            self.m3u8_file.unlink(missing_ok=True)
        if self.adquired_semaphore:
            self.sem.release()

    async def multidown(self, tries: int, segment: int) -> bool:
        assert self.content is not None

        count = 0

        for _ in tries_iterator(tries):
            try:
                with self.files[segment].open("wb") as f:
                    async for chunk in self.content[segment]():
                        if chunk is None:
                            break

                        if self.estimate:
                            self.estimate.add(len(chunk))

                        f.write(chunk)

                        count += len(chunk)
                        self.received += len(chunk)

                        self.update_status()

                    debug_log(
                        f"finished segment {segment} {count}/{self.sizes[segment]}", 1
                    )
                    if count == self.sizes[segment]:
                        self.completed[segment] = True
                        return True
            except Exception:
                debug_log("========================================================", 1)
                debug_log(
                    f"[{self.download_id}] Error while downloading segment {segment}",
                    1,
                )
                debug_log(f"", 1)
                debug_log(traceback.format_exc(), 1)

            self.received -= count
        return False

    def update_status(self, force: bool = False):
        current = time.time()
        if (current - self.last_status_update) > 0.1 or force:
            self.last_status_update = current
            with self.printr.get_lock():
                self.printr.set(self.download_id + "_progress", self.received)
                if self.estimate:
                    self.printr.set(
                        self.download_id + "_perc", (100 * self.received) / self.size
                    )
                else:
                    self.printr.set(self.download_id + "_perc", math.nan)
                self.printr.set(
                    self.download_id + "_timer",
                    delta_time_str(self.start_time, current),
                )
