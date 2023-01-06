import math
import os
import subprocess
import threading
import time
import traceback
from typing import Any, Callable, Generator

import m3u8
import requests

from printer import FakePrinter, PrinterType
from utils.debugging import debug_log
from utils.format import delta_time_str, format_time
from utils.prediction import Prediction

SrcType = Callable[[int], tuple[Generator[Any, None, None],
                                int, int, Callable[[str, str], None]]]


def http_builder(url: str, headers: dict[str, str | bytes] | None = None) -> SrcType:
    def src(_: int):
        with requests.head(url, timeout=3 * 60, headers=headers, allow_redirects=True) as r:
            # debug_log(url + " status_code: " + str(r.status_code))
            r.raise_for_status()
            content_length = r.headers.get('content-length')
            if content_length is not None:
                total_length = int(content_length)
                total = (total_length // 1024) + 1
            else:
                total = -1

        def stream():
            with requests.get(url, stream=True, timeout=3 * 60, headers=headers, allow_redirects=True) as r:
                r.raise_for_status()
                for chunck in r.iter_content(chunk_size=1024):
                    yield chunck

        def func(folder: str, filename: str): return None
        return stream(), 0, total, func
    return src


def m3u8_builder(playlist_url: str, headers: dict[str, str | bytes] | None = None, p: PrinterType | None = None) -> SrcType:
    def get_real_url(url: str):
        return url
        # playlists = m3u8.load(uri=url, headers=headers).playlists
        # while playlists[0].stream_info.resolution[1] >= 1080:
        #     playlists.pop(0)
        # return playlists[0].absolute_uri

    def ffmpegCorrection(folder: str, filename: str):
        tmp_path = os.path.join(folder, "_"+filename)
        correct_path = os.path.join(folder, filename)
        subprocess.run(["ffmpeg", "-y", "-hwaccel", "cuda", "-i", correct_path, tmp_path],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL
                       )
        os.remove(correct_path)
        os.rename(tmp_path, correct_path)

    real_url = get_real_url(playlist_url)
    playlist = m3u8.load(uri=real_url, headers=headers)
    if p:
        p.print(playlist.segments)
    n = len(playlist.segments)

    def stream(segments_processed: int):
        i = segments_processed
        for seg in playlist.segments[segments_processed:]:
            if p:
                p.print("processing segment", i)
                i += 1
            with requests.get(seg.absolute_uri, headers=headers, stream=False, timeout=3 * 60) as r:
                r.raise_for_status()
                data = r.content
                yield data
    return lambda segments_processed: (stream(segments_processed), segments_processed, n, ffmpegCorrection)


_download_N: int = 0
_download_N_lock: threading.Lock = threading.Lock()


def download_file(*, src: SrcType,
                  folder: str,
                  filename: str,
                  desc: str = "",
                  remove_old: bool = True,
                  max_tries: int = 10,
                  printr: PrinterType | None = None,
                  size_digits: int = 6,
                  cb: Callable[[str, bool, Any], None] | None = None,
                  cb_data: Any = None
                  ) -> tuple[str, bool]:
    global _download_N
    if desc == "":
        desc = filename
    temp_filename = os.path.join(folder, filename + ".part")
    local_filename = os.path.join(folder, filename)
    success = False
    with _download_N_lock:
        _download_N += 1
        download_id = "Download_N" + str(_download_N)
    file_stats: dict[str, float | str] = {
        "progress": 0,
        "max": 0,
        "perc": 0,
        "try": 0,
        "estimated": format_time(0),
        "timer": format_time(0),
        "updated": time.asctime(),
    }
    if printr is None:
        printr = FakePrinter()

    printr.set(download_id, file_stats)
    msg = f"{desc}:"
    msg += "{" + download_id + "[progress]:" + str(size_digits) + "d}|"
    msg += "{" + download_id + "[max]:" + str(size_digits) + "d}"
    msg += "({" + download_id + "[perc]:6.2f}%)"
    msg += "[{" + download_id + "[try]}] "
    msg += "{" + download_id + "[timer]} "
    msg += "{" + download_id + "[estimated]} "
    msg += "Last changed at {" + download_id + "[updated]}\n"
    printr.add_desc(msg)

    segments_processed = 0
    start = time.perf_counter()
    estimate = t = None
    transformer: Callable[[str, str], None] = lambda _, __: None
    for try_ in range(max_tries):
        file_stats["try"] = try_
        file_stats["updated"] = time.asctime()
        printr.set(download_id, file_stats)
        estimate = t = None
        try:
            # printr.print(segments_processed)
            stream, segments_processed, total, transformer = src(
                segments_processed)
            mode = 'ab' if segments_processed > 0 else 'wb'
            if total > 0:
                estimate = Prediction(printr, download_id, total)
                estimate.segments_processed = segments_processed
                t = threading.Thread(target=estimate.run)
                t.start()
            # printr.print(mode)
            with open(temp_filename, mode) as f:
                file_stats["max"] = total
                printr.set(download_id, file_stats)
                for chunk in stream:
                    segments_processed += 1
                    if estimate:
                        estimate.add()
                        file_stats["perc"] = (segments_processed / total) * 100
                    else:
                        file_stats["perc"] = math.nan
                    file_stats["timer"] = delta_time_str(
                        start, time.perf_counter())
                    file_stats["progress"] = segments_processed
                    file_stats["updated"] = time.asctime()
                    printr.set(download_id, file_stats)
                    if chunk:
                        f.write(chunk)
                        f.flush()
            success = segments_processed > 0 and (
                True if total < 0 else segments_processed == total)
            break
        except Exception as e:
            if estimate and t:
                estimate.stop()
                t.join()
            # printr.print(e)
            # printr.print(traceback.format_exc())
            debug_log(e)
            debug_log(traceback.format_exc())
            file_stats["progress"] = 0
            file_stats["max"] = 0
            file_stats["perc"] = 0
            file_stats["timer"] = delta_time_str(start, time.perf_counter())
            file_stats["updated"] = time.asctime()
            printr.set(download_id, file_stats)
            time.sleep(5)
            if try_ != (max_tries - 1) and try_ != 0 and try_ % 5 == 0:
                time.sleep(1 * 60)
    if estimate and t:
        estimate.stop()
        t.join()

    if remove_old:
        try:
            os.remove(local_filename)
        except:
            pass

    if success:
        os.rename(temp_filename, local_filename)
        try_ = file_stats["try"]
        file_stats["try"] = "transforming"
        file_stats["updated"] = time.asctime()
        file_stats["estimated"] = format_time(0)
        printr.set(download_id, file_stats)
        transformer(folder, filename)
        file_stats["updated"] = time.asctime()
        file_stats["try"] = try_
        printr.set(download_id, file_stats)
    else:
        debug_log("processed " + str(segments_processed) + "segments")
        file_stats["progress"] = -1
        file_stats["max"] = -1
        file_stats["perc"] = -1
        file_stats["timer"] = delta_time_str(start, time.perf_counter())
        file_stats["estimated"] = format_time(0)
        file_stats["updated"] = time.asctime()
        printr.set(download_id, file_stats)

    if cb:
        cb(local_filename, success, cb_data)
    return (temp_filename, success)