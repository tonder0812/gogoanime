import os
import sys
import threading
import time
import traceback

import requests

from anime import AnimeInfo, get_anime_info
from config import download_path, quit_location
from cookies import load_cookies
from downloader import download_anime
from printer import Printer
from saving import Processing
from saving import get_watching as _get_watching
from saving import with_processing

CHECK_INTERVAL: int = 60 * 5

threads: list[threading.Thread] = []
processing = Processing()
names: dict[str, str] = {}
infos: dict[str, AnimeInfo] = {}


@with_processing(processing)
def set_processing():
    p.set("processing", str(processing))


@with_processing(processing)
def get_watching(names: dict[str, str]) -> dict[str, list[str]]:
    res = _get_watching(names, processing)
    set_processing()
    return res


def invalid_info(anime_link: str):
    return anime_link not in infos or infos[anime_link].logo_url is None


def update_info(anime_link: str):
    if invalid_info(anime_link):
        info = get_anime_info(session, anime_link)
        if info is None:
            return
        infos[anime_link] = info


@ with_processing(processing)
def check():
    watching = get_watching(names)
    for anime_link in watching:
        time.sleep(1)
        os.system("title checking "+anime_link)

        update_info(anime_link)

        if invalid_info(anime_link):
            continue

        download_anime(
            session=session,
            base_path=download_path,
            anime_link=anime_link,
            watched_eps=watching[anime_link],
            infos=infos,
            names=names,
            p=p,
            threads=threads,
            processing=processing
        )
        set_processing()


def raise_for_quit():
    with open(quit_location, "r") as f:
        stop = f.read()
    if len(stop) > 0:
        os.system("title quiting")
        p.print("break")
        with open(quit_location, "w") as f:
            pass
        raise Exception()


session = requests.Session()
session.cookies.update(load_cookies())

p: Printer = Printer()

p.set("timer", CHECK_INTERVAL)
p.set("processing", str(processing))

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
            check()
        except Exception as e:
            p.print("Check failed:")
            p.print(e)
            p.print(traceback.format_exc())
        if "-c" not in sys.argv:
            break
        for i in range(CHECK_INTERVAL):
            get_watching(names)

            raise_for_quit()

            os.system(f"title checking in {CHECK_INTERVAL-i}s")
            p.set("timer", CHECK_INTERVAL - i)
            time.sleep(1)
except Exception as e:
    pass
finally:
    for t in threads:
        t.join()
    get_watching(names)
    p.stop()
