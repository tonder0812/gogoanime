import os
import threading
import time
from typing import Any, Callable

import requests

from anime import AnimeInfo, get_anime_info
from config import user_end_download, user_start_downloading, max_tries
from episode import episode_order, get_episodes_to_download
from printer import FakePrinter, AbstractPrinter
from saving import Processing
from utils.download import SrcType, download_file, http_builder
from utils.format import generate_filenames, normalize_filename


def anime_logo_builder(anime_id: str, infos: dict[str, AnimeInfo], session: requests.Session) -> SrcType:
    last_link = [""]

    def src(segments_processed: int):
        if last_link[0] == "":
            info = infos[anime_id]
        else:
            info = get_anime_info(session, anime_id)

        while info is None or info.logo_url is None:
            info = get_anime_info(session, anime_id)

        if info.logo_url != last_link[0]:
            segments_processed = 0

        last_link[0] = info.logo_url

        return http_builder(info.logo_url, session=session)(segments_processed)
    return src


def dowload_anime_logo(p: AbstractPrinter, session: requests.Session, infos: dict[str, AnimeInfo], anime_id: str, show_folder: str, threads: list[threading.Thread], minimize_print: bool = False) -> None:
    if not os.path.isfile(os.path.join(show_folder, "logo.png")):
        t = threading.Thread(target=download_file, kwargs={
            "src": anime_logo_builder(anime_id, infos, session),
            "folder": show_folder,
            "filename": "logo.png",
            "printr": p,
            "size_digits": 2,
            "max_tries": -1
        })
        t.start()
        threads.append(t)


def download_callback(anime_id: str, ep: str, processing: Processing | None) -> Callable[[str, bool, Any, str], None]:
    def cb(filename: str, success: bool, data: Any, _: str):
        if processing is not None:
            processing.finish(anime_id, ep, success)
        user_end_download(filename, success, data)
    return cb


CallbackType = Callable[[str, str, Processing | None], Callable[[str, bool, Any, str], None]]


def download_episode(*,
                     anime_name: str,
                     anime_id: str,
                     anime_folder: str,
                     download_url: str,

                     ep: str,
                     epN: int,
                     eps: list[str],

                     p: AbstractPrinter | None = None,
                     session: requests.Session | None = None,
                     threads: list[threading.Thread] | None = None,
                     processing: Processing | None = None,
                     callback: CallbackType | None = None
                     ):
    if threads is None:
        threads = []

    if callback is None:
        callback = download_callback

    if p is None:
        p = FakePrinter()

    user_start_downloading(anime_name, ep)

    filename, filenameDesc = generate_filenames(eps, epN, ep)

    if processing is not None:
        processing.start(anime_id, ep)

    t = threading.Thread(target=download_file,
                         args=[],
                         kwargs={
                             "src": http_builder(download_url, session=session),
                             "folder": anime_folder,
                             "filename": filename,
                             "desc": filenameDesc,
                             "max_tries": max_tries,
                             "printr": p,
                             "size_digits": 6,
                             "cb": callback(anime_id, ep, processing),
                             "cb_data": f"{anime_name} - {ep}\n"
                         })
    t.start()
    threads.append(t)
    time.sleep(1)


def download_anime(
        *,
        session: requests.Session,
        base_path: str,
        anime_id: str,
        blacklist: list[str] | None = None,
        whitelist: list[str] | None = None,
        infos: dict[str, AnimeInfo],
        names: dict[str, str],

        p: AbstractPrinter,
        threads: list[threading.Thread],
        processing: Processing | None,
        callback: CallbackType | None = None
) -> bool:
    if processing is not None:
        if blacklist is None:
            blacklist = []
        blacklist.extend(processing.get_eps(anime_id))

    links, links_to_download = get_episodes_to_download(
        session,
        infos[anime_id].anime_id, blacklist, whitelist
    )

    if links is None or links_to_download is None or len(links_to_download) <= 0:
        return False

    anime_name = names.get(anime_id, infos[anime_id].name)

    eps: list[str] = list(sorted(links.keys(), key=episode_order))

    p.print("\n"+anime_name)
    p.print(f"{len(eps)} ep(s):")
    for ep in eps:
        p.add_desc("  episode " + ep)
        if links_to_download.get(ep) is not None:
            p.add_desc(" V")
        p.print("")

    anime_folder = os.path.join(
        base_path, normalize_filename(anime_name, False))

    os.makedirs(anime_folder, exist_ok=True)

    dowload_anime_logo(p, session, infos, anime_id,
                       anime_folder, threads, True)

    for epN, ep in enumerate(eps, 1):
        download_url = links_to_download.get(ep)
        if download_url is None:
            continue

        download_episode(
            anime_name=anime_name,
            anime_id=anime_id,
            anime_folder=anime_folder,
            download_url=download_url,

            ep=ep,
            epN=epN,
            eps=eps,

            p=p,
            session=session,
            threads=threads,
            processing=processing,
            callback=callback
        )
    return True
