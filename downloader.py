import os
import threading
from typing import Any, Callable

import requests

from anime import AnimeInfo
from config import user_end_download, user_start_downloading
from episode import ep_order, get_episode_to_download
from printer import FakePrinter
from printer.printer import PrinterType
from saving import Processing
from utils.download import download_file, http_builder
from utils.format import generate_filenames, normalize_filename


def dowload_anime_logo(p: PrinterType, show_info: AnimeInfo, show_folder: str, threads: list[threading.Thread], minimize_print: bool = False) -> None:
    image_link = "Logo already exists"
    if show_info.logo_url is None:
        p.print("Failed to get logo url")
        return
    if not os.path.isfile(os.path.join(show_folder, "logo.png")):
        image_link = show_info.logo_url
        t = threading.Thread(target=download_file, kwargs={
            "src": http_builder(image_link),
            "folder": show_folder,
            "filename": "logo.png",
            "printr": p,
            "size_digits": 2})
        t.start()
        threads.append(t)
    if not minimize_print:
        p.print(image_link)


def download_callback(anime_link: str, ep: str, processing: Processing | None) -> Callable[[str, bool, Any], None]:
    def cb(filename: str, success: bool, data: Any):
        if processing is not None:
            with processing.lock:
                tmp = {k: v for k, v in processing[anime_link].items()}
                if success:
                    tmp[ep] = True
                else:
                    del tmp[ep]
                processing[anime_link] = tmp
        user_end_download(filename, success, data)
    return cb


def download_episode(
        anime_name: str,
        anime_link: str,
        anime_folder: str,
        download_url: str,

        ep: str,
        epN: int,
        eps: list[str],

        p: PrinterType | None = None,
        threads: list[threading.Thread] | None = None,
        processing: Processing | None = None,
):
    if threads is None:
        threads = []

    if p is None:
        p = FakePrinter()

    user_start_downloading(anime_name, ep)

    filename, filenameDesc = generate_filenames(eps, epN, ep)

    if processing is not None:
        with processing.lock:
            tmp = processing[anime_link]
            tmp[ep] = False
            processing[anime_link] = tmp

    t = threading.Thread(target=download_file,
                         args=[],
                         kwargs={
                             "src": http_builder(download_url),
                             "folder": anime_folder,
                             "filename": filename,
                             "desc": filenameDesc,
                             "max_tries": 100,
                             "printr": p,
                             "size_digits": 6,
                             "cb": download_callback(anime_link, ep, processing),
                             "cb_data": f"{anime_name} - {ep}\n"
                         })
    t.start()
    threads.append(t)


def download_anime(
        session: requests.Session,
        base_path: str,
        anime_link: str,
        watched_eps: list[str],
        infos: dict[str, AnimeInfo],
        names: dict[str, str],

        p: PrinterType,
        threads: list[threading.Thread],
        processing: Processing,
):

    with processing.lock:
        links, links_to_download = get_episode_to_download(
            session,
            infos[anime_link].anime_id,
            watched_eps +
            list(processing.get(anime_link, {}))
        )

    if links is None or links_to_download is None or len(links_to_download) <= 0:
        return

    anime_name = names.get(anime_link, infos[anime_link].name)

    with processing.lock:
        processing[anime_link] = processing.get(anime_link, {})

    eps: list[str] = list(sorted(links.keys(), key=ep_order))

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

    dowload_anime_logo(p, infos[anime_link],
                       anime_folder, threads, True)

    for epN, ep in enumerate(eps, 1):
        download_url = links_to_download.get(ep)
        if download_url is None:
            continue

        download_episode(
            anime_name=anime_name,
            anime_link=anime_link,
            anime_folder=anime_folder,
            download_url=download_url,

            ep=ep,
            epN=epN,
            eps=eps,

            p=p,
            threads=threads,
            processing=processing,
        )
    p.add_desc("\nTime to next check:{timer}s\n")
    p.print("----------------------------")
