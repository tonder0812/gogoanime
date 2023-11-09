if __name__ == "__main__":
    import sys

    sys.path.insert(0, "..")

import asyncio
import threading
import time
import traceback
from inspect import getfullargspec
from pathlib import Path
from typing import Callable, TypeVar
from printer import AbstractPrinter, FakePrinter
from utils.asyncio_downloader import DownloadTask, SrcGeneratorType, tries_iterator
from utils.debugging import debug_log
from utils.format import format_time

_download_N: int = 0
_download_N_lock: threading.Lock = threading.Lock()

T = TypeVar("T")


async def run_download(
    task: DownloadTask,
    full_tries: int,
    inner_tries: int,
    cb: Callable[[T], None] | None = None,
    cb_data: T = None,
) -> bool:
    first = True
    for try_ in tries_iterator(full_tries):
        task.printr.set(task.download_id + "_try", try_)
        try:
            if not await task.setup(inner_tries):
                break

            if first:
                if cb is not None:
                    cb(cb_data)
                first = False

            async with asyncio.TaskGroup() as tg:
                for i in range(task.segments):
                    tg.create_task(task.multidown(inner_tries, i))

            if all(task.completed):
                return True
        finally:
            task.stop()
    return False


def download_file(
    *,
    src: SrcGeneratorType,
    folder: Path,
    filename: str,
    desc: str = "",
    remove_old: bool = True,
    max_full_tries: int = 50,
    max_inner_tries: int = 50,
    segments: int = 10,
    printr: AbstractPrinter | None = None,
    size_digits: int = 9,
    cb_start: (Callable[[T], None] | None) = None,
    cb_end: (Callable[[Path, bool, T, str], None] | None) = None,
    cb_data: T = None,
    download_id: str | None = None,
) -> tuple[Path, bool]:
    global _download_N

    if desc == "":
        desc = filename

    temp_filename = folder / (filename + ".part")
    local_filename = folder / filename

    success = False
    repeating_download = True

    if download_id is None:
        with _download_N_lock:
            _download_N += 1
            download_id = "Download_N" + str(_download_N)
        repeating_download = False

    if printr is None:
        printr = FakePrinter()

    printr.set(download_id + "_progress", 0)
    printr.set(download_id + "_max", 0)
    printr.set(download_id + "_perc", 0)
    printr.set(download_id + "_try", 0)
    printr.set(download_id + "_estimated", format_time(0))
    printr.set(download_id + "_timer", format_time(0))
    printr.set(download_id + "_updated", time.asctime())
    if not repeating_download:
        msg = "{" + download_id + "_progress:" + str(size_digits) + "d}|"
        msg += "{" + download_id + "_max:" + str(size_digits) + "d}"
        msg += "({" + download_id + "_perc:6.2f}%)"
        msg += "[{" + download_id + "_try}] "
        msg += "{" + download_id + "_timer} "
        msg += "{" + download_id + "_estimated} "
        msg += "Last changed at {" + download_id + "_updated}\n"
        with printr.get_lock():
            printr.print(f"{desc}:", end="")
            printr.add_desc(msg)

    task = DownloadTask(
        src=src,
        filename=temp_filename,
        printr=printr,
        download_id=download_id,
        segments=segments,
    )
    try:
        success = asyncio.run(
            run_download(task, max_full_tries, max_inner_tries, cb_start, cb_data)
        )
    except Exception as e:
        debug_log("========================================================")
        debug_log(e)
        debug_log(traceback.format_exc())
    if remove_old:
        for _ in tries_iterator(max_full_tries):
            try:
                local_filename.unlink(missing_ok=True)
                break
            except Exception as e:
                debug_log("========================================================")
                debug_log(e)
                debug_log(traceback.format_exc())
            time.sleep(0.1)
        else:
            success = False

    if success:
        temp_filename.rename(local_filename)
    else:
        printr.set(download_id + "_progress", -1)
        printr.set(download_id + "_max", -1)
        printr.set(download_id + "_perc", -1)
        printr.set(download_id + "_try", -1)
        printr.set(download_id + "_estimated", format_time(0))
        debug_log("========================================================")
        debug_log(download_id)
        debug_log(task.completed)
        debug_log(task.filename)
        debug_log(task.ranges)
        debug_log(task.received)
        debug_log(task.segments)
        debug_log(task.size)
    if cb_end:
        cb_end(local_filename, success, cb_data, download_id)

    return (temp_filename, success)


def download_file_threaded(
    *,
    src: SrcGeneratorType,
    folder: Path,
    filename: str,
    desc: str = "",
    remove_old: bool = True,
    segments: int = 10,
    max_full_tries: int = 50,
    max_inner_tries: int = 50,
    printr: AbstractPrinter | None = None,
    size_digits: int = 9,
    cb_start: (Callable[[T], None] | None) = None,
    cb_end: (Callable[[Path, bool, T, str], None] | None) = None,
    cb_data: T = None,
    download_id: str | None = None,
) -> threading.Thread:
    # def download(**kwargs:Any):
    #     asyncio.run(download_file(**kwargs))
    return threading.Thread(
        target=download_file,
        kwargs={
            "src": src,
            "folder": folder,
            "filename": filename,
            "desc": desc,
            "remove_old": remove_old,
            "max_full_tries": max_full_tries,
            "max_inner_tries": max_inner_tries,
            "segments": segments,
            "printr": printr,
            "size_digits": size_digits,
            "cb_start": cb_start,
            "cb_end": cb_end,
            "cb_data": cb_data,
            "download_id": download_id,
        },
    )


annotations_normal = getfullargspec(download_file).annotations
annotations_normal.pop("return", None)
annotations_thread = getfullargspec(download_file_threaded).annotations
annotations_thread.pop("return", None)
assert (
    annotations_normal == annotations_thread
), "download_file and download_file_threaded must have the same arguments"


if __name__ == "__main__":
    from utils.asyncio_downloader import httpx_ranged_builder
    from printer import Printer

    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <url> <filename> [<segments>]")
        exit(1)

    segments = 10
    if len(sys.argv) > 3:
        segments = int(sys.argv[3])
    p = Printer()
    try:
        path = Path(sys.argv[2])
        download_file(
            src=httpx_ranged_builder(sys.argv[1]),
            folder=path.parent,
            filename=path.name,
            segments=segments,
            printr=p,
        )
    finally:
        p.stop()
