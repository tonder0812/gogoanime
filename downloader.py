import os
import threading
import time
from pathlib import Path
from typing import Any, Callable

import httpx

from anime import AnimeInfo, get_anime_info
from config import (
    max_full_tries,
    max_inner_tries,
    segments,
    user_end_download,
    user_start_downloading,
)
from episode import episode_order, get_episodes_to_download
from printer import AbstractPrinter, FakePrinter
from saving import Processing
from utils.asyncio_downloader import SrcGeneratorType, SrcType, httpx_ranged_builder
from utils.download import download_file_threaded
from utils.format import generate_filenames, normalize_filename


def anime_logo_builder(
    anime_id: str, infos: dict[str, AnimeInfo], client: httpx.Client
) -> SrcGeneratorType:
    last_link = [""]

    async def src(tries: int) -> SrcType:
        if last_link[0] == "":
            info = infos[anime_id]
        else:
            info = get_anime_info(client, anime_id)

        while info is None or info.logo_url is None:
            info = get_anime_info(client, anime_id)

        last_link[0] = info.logo_url

        newClient = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=None, max_keepalive_connections=None),
            follow_redirects=True,
        )
        newClient.cookies = client.cookies

        builder = httpx_ranged_builder(info.logo_url, client=newClient)
        return await builder(tries)

    return src


def dowload_anime_logo(
    p: AbstractPrinter,
    client: httpx.Client,
    infos: dict[str, AnimeInfo],
    anime_id: str,
    show_folder: Path,
    threads: list[threading.Thread],
) -> None:
    if not os.path.isfile(os.path.join(show_folder, "logo.png")):
        t = download_file_threaded(
            src=anime_logo_builder(anime_id, infos, client),
            folder=show_folder,
            filename="logo.png",
            printr=p,
            size_digits=2,
            max_full_tries=-1,
        )
        t.start()
        threads.append(t)


def download_callback(
    anime_id: str, ep: str, processing: Processing | None
) -> Callable[[Path, bool, Any, str], None]:
    def cb(filename: Path, success: bool, data: Any, _: str):
        if processing is not None:
            processing.finish(anime_id, ep, success)
        user_end_download(filename, success, data)

    return cb


CallbackType = Callable[
    [str, str, Processing | None], Callable[[Path, bool, Any, str], None]
]


def download_episode(
    *,
    anime_name: str,
    anime_id: str,
    anime_folder: Path,
    download_url: str,
    ep: str,
    epN: int,
    eps: list[str],
    p: AbstractPrinter | None = None,
    client: httpx.Client | None = None,
    threads: list[threading.Thread] | None = None,
    processing: Processing | None = None,
    callback: CallbackType | None = None,
):
    if threads is None:
        threads = []

    if callback is None:
        callback = download_callback

    if p is None:
        p = FakePrinter()

    filename, filename_desc = generate_filenames(eps, epN, ep)

    if processing is not None:
        processing.start(anime_id, ep)

    newClient = httpx.AsyncClient(
        limits=httpx.Limits(max_connections=None, max_keepalive_connections=None),
        follow_redirects=True,
    )
    if client:
        newClient.cookies = client.cookies

    t = download_file_threaded(
        src=httpx_ranged_builder(download_url, client=newClient),
        folder=anime_folder,
        filename=filename,
        desc=filename_desc,
        max_full_tries=max_full_tries,
        max_inner_tries=max_inner_tries,
        segments=segments,
        printr=p,
        size_digits=9,
        cb_start=user_start_downloading,
        cb_end=callback(anime_id, ep, processing),
        cb_data=f"{anime_name} - {ep}\n",
    )
    t.start()
    threads.append(t)
    time.sleep(1)


def download_anime(
    *,
    client: httpx.Client,
    base_path: Path,
    anime_id: str,
    blacklist: list[str] | None = None,
    whitelist: list[str] | None = None,
    infos: dict[str, AnimeInfo],
    names: dict[str, str],
    p: AbstractPrinter,
    threads: list[threading.Thread],
    processing: Processing | None,
    callback: CallbackType | None = None,
) -> bool:
    if processing is not None:
        if blacklist is None:
            blacklist = []
        blacklist.extend(processing.get_eps(anime_id))

    links, links_to_download = get_episodes_to_download(
        client, infos[anime_id].anime_id, blacklist, whitelist
    )

    if links is None or links_to_download is None or len(links_to_download) <= 0:
        return False

    anime_name = names.get(anime_id, infos[anime_id].name)

    eps: list[str] = list(sorted(links.keys(), key=episode_order))

    p.print("\n" + anime_name)
    p.print(f"{len(eps)} ep(s):")
    for ep in eps:
        p.add_desc("  episode " + ep)
        if links_to_download.get(ep) is not None:
            p.add_desc(" V")
        p.print("")

    anime_folder = base_path / normalize_filename(anime_name, False)

    os.makedirs(anime_folder, exist_ok=True)

    dowload_anime_logo(p, client, infos, anime_id, anime_folder, threads)

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
            client=client,
            threads=threads,
            processing=processing,
            callback=callback,
        )
    return True
