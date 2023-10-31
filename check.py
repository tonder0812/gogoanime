import os
import sys
import threading
import time
import traceback

import httpx

from anime import AnimeInfo, get_anime_info
from config import download_path, quit_location
from cookies import load_cookies
from downloader import download_anime
from printer import AbstractPrinter, Printer
from saving import Processing
from saving import get_watching as _get_watching

CHECK_INTERVAL: int = 60 * 5

threads: list[threading.Thread] = []
processing = Processing()
names: dict[str, str] = {}
infos: dict[str, AnimeInfo] = {}


@processing.with_lock
def set_processing(processing: Processing, p: AbstractPrinter):
    p.set("processing", str(processing))


@processing.with_lock
def get_watching(
    processing: Processing, p: AbstractPrinter, names: dict[str, str]
) -> dict[str, list[str]]:
    res = _get_watching(names, processing)
    set_processing(p)
    return res


def invalid_info(anime_id: str):
    return anime_id not in infos or infos[anime_id].logo_url is None


def update_info(client: httpx.Client, anime_id: str):
    if invalid_info(anime_id):
        info = get_anime_info(client, anime_id)
        if info is None:
            return
        infos[anime_id] = info


@processing.with_lock
def check(processing: Processing, p: AbstractPrinter, client: httpx.Client):
    watching = get_watching(p, names)
    for anime_id in watching:
        time.sleep(1)
        os.system("title checking " + anime_id)

        update_info(client, anime_id)

        if invalid_info(anime_id):
            continue

        if download_anime(
            client=client,
            base_path=download_path,
            anime_id=anime_id,
            blacklist=watching[anime_id],
            infos=infos,
            names=names,
            p=p,
            threads=threads,
            processing=processing,
        ):
            p.add_desc("\nTime to next check:{timer}s\n")
            p.print("----------------------------")
        set_processing(p)


def raise_for_quit(p: AbstractPrinter):
    with open(quit_location, "r") as f:
        stop = f.read()
    if len(stop) > 0:
        os.system("title quiting")
        p.print("break")
        with open(quit_location, "w") as f:
            pass
        raise Exception()


def main():
    p = Printer()

    client = httpx.Client(
        limits=httpx.Limits(max_connections=None, max_keepalive_connections=None),
        follow_redirects=True,
    )
    client.cookies.update(load_cookies())

    p.set("timer", CHECK_INTERVAL)

    set_processing(p)

    p.print()
    p.add_desc("Time to next check:{timer}s ")
    p.add_desc("[processing: {processing}]\n")
    p.print("========================")
    p.print("LOGS:")
    p.print("----------------------------")
    try:
        while True:
            p.set("timer", CHECK_INTERVAL)
            os.system("title checking")
            try:
                check(p, client)
            except Exception as e:
                p.print("Check failed:")
                p.print(e)
                p.print(traceback.format_exc())
            if "-c" not in sys.argv:
                break
            for i in range(CHECK_INTERVAL):
                get_watching(p, names)

                raise_for_quit(p)

                os.system(f"title checking in {CHECK_INTERVAL-i}s")
                p.set("timer", CHECK_INTERVAL - i)
                time.sleep(1)
    except Exception as e:
        pass
    finally:
        for t in threads:
            t.join()
        get_watching(p, names)
        p.stop()


if __name__ == "__main__":
    main()
