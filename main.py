import sys
import threading
from pathlib import Path
from typing import Any, Callable

import httpx

from anime import get_anime_info
from config import download_path, user_end_download
from cookies import load_cookies
from downloader import download_anime
from printer import AbstractPrinter, Printer
from saving import Processing


def input_ep_list(p: AbstractPrinter, typ: str, lst: list[str]):
    p.print(f"{typ} ep ids: (leave blank to stop inputing)")
    ep = p.input()
    while ep.strip() != "":
        lst.append(ep)
        ep = p.input()


def callback(
    anime_id: str, ep: str, processing: Processing | None
) -> Callable[[Path, bool, Any, str], None]:
    def cb(filename: Path, success: bool, data: Any, _: str):
        user_end_download(filename, success, data)
        if processing is not None:
            processing.finish(anime_id, ep, success)
        if not success:
            threads: list[threading.Thread] = []
            info = get_anime_info(client, anime_id)
            while info is None:
                info = get_anime_info(client, anime_id)
            download_anime(
                client=client,
                base_path=base_path,
                anime_id=anime_id,
                blacklist=blacklist,
                whitelist=whitelist,
                infos={anime_id: info},
                names={},
                p=p,
                threads=threads,
                processing=processing,
                callback=callback,
            )
            for t in threads:
                t.join()

    return cb


p: AbstractPrinter = Printer()
client = httpx.Client()
blacklist: list[str] | None = None
whitelist: list[str] | None = None
base_path: Path = download_path


def main():
    global blacklist, whitelist, base_path
    args: list[str] = sys.argv

    anime_id: str = ""

    threads: list[threading.Thread] = []

    processing = Processing()

    try:
        while len(args) > 0:
            arg = args.pop(0)

            if arg == "-id" and len(args) > 0:
                anime_id = args[0]
                args.pop(0)
            elif arg == "-place" and len(args) > 0:
                base_path = Path(args[0])
                args.pop(0)
            elif arg == "-Iwhitelist":
                if whitelist is None:
                    whitelist = []
                input_ep_list(p, "whitelist", whitelist)
            elif arg == "-Iblacklist":
                if blacklist is None:
                    blacklist = []
                input_ep_list(p, "blacklist", blacklist)
            elif arg == "-Cwhitelist":
                if whitelist is None:
                    whitelist = []
                while len(args) > 0 and len(args[0]) > 0 and args[0][0] != "-":
                    whitelist.append(args[0])
                    args.pop(0)
            elif arg == "-Cblacklist":
                if blacklist is None:
                    blacklist = []
                while len(args) > 0 and len(args[0]) > 0 and args[0][0] != "-":
                    blacklist.append(args[0])
                    args.pop(0)

        if anime_id == "":
            p.print("please provide the anime id")
            return

        if not base_path.exists() or not base_path.is_dir():
            p.print("Download folder must exist")

        client.cookies.update(load_cookies())

        info = get_anime_info(client, anime_id)
        while info is None:
            info = get_anime_info(client, anime_id)

        download_anime(
            client=client,
            base_path=base_path,
            anime_id=anime_id,
            blacklist=blacklist,
            whitelist=whitelist,
            infos={anime_id: info},
            names={},
            p=p,
            threads=threads,
            processing=processing,
            callback=callback,
        )
    except Exception:
        pass
    finally:
        for t in threads:
            t.join()
        p.stop()


if __name__ == "__main__":
    main()
