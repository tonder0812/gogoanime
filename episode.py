import string
import httpx

from config import animenosub_domain
from parsers import EpListParser
from parsers.common import Parser
from parsers.video_link import VideoProviderLinkParser
import re
from config import max_full_tries
import m3u8


def int2base(x: int, base: int, digs: str = string.digits + string.ascii_letters):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits: list[str] = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append("-")

    digits.reverse()

    return "".join(digits)


def decode_Moon_m3u8(data: str):
    matches = re.findall(
        r"}\('(.*?[^\\])'\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*'(.*?[^\\])'", data
    )
    assert len(matches) == 1
    matc: tuple[str, str, str, str] = matches[0]
    assert isinstance(matc, tuple)
    p, a, c, k = matc
    assert isinstance(p, str)
    assert isinstance(a, str)
    assert isinstance(c, str)
    assert isinstance(k, str)
    a = int(a)
    c = int(c)
    k = k.split("|")
    while c >= 0:
        c -= 1
        if k[c]:
            r = re.compile(rf"\b{int2base(c,a)}\b")
            p = r.sub(k[c], p)
    m3u8_matches = re.findall(r"sources:\s*\[\s*{\s*file:\s*\"(.*?)\"", p)
    assert len(m3u8_matches) == 1
    m3u8_match = m3u8_matches[0]
    assert isinstance(m3u8_match, str)
    return m3u8_match


class MoonM3u8Parser(Parser):
    def __init__(self, contents: str) -> None:
        super().__init__(contents)
        self.m3u8_link: str | None = None

    def handle_data(self, data: str) -> None:
        data = data.strip()
        if self.curent_tag.tag == "script" and data.startswith("eval"):
            self.m3u8_link = decode_Moon_m3u8(data)


def get_episode_download_link(
    client: httpx.Client, links: dict[str, str], episode: str
) -> tuple[str, str] | None:
    try:
        r = client.get(
            links[episode],
            headers={
                "Accept-Language": "en-GB,en;q=0.5",
            },
        )
        r.raise_for_status()
        with VideoProviderLinkParser(r.content.decode()) as p:
            print(p.link)
            if p.link is None:
                return None
            r4 = httpx.get(
                p.link,
                headers={
                    # "User-Agent": "Chrome",
                    "Accept-Language": "en-GB,en;q=0.5",
                },
            )
            if "location" in r4.headers:
                r4 = httpx.get(
                    r4.headers["location"],
                    headers={
                        # "User-Agent": "Chrome",
                        "Accept-Language": "en-GB,en;q=0.5",
                    },
                )
            # debug_log(f"moon content: {r4.content.decode()}")
            matches = re.findall('iframe src="(.*?)"', r4.content.decode())
            # assert len(matches) == 1
            if len(matches) != 1:
                return None
            real_link = matches[0]
            assert isinstance(real_link, str)
            if real_link.startswith("//"):
                real_link = "https:" + real_link
            main_url: str | None = None
            for _ in range(max_full_tries):
                r2 = client.get(
                    real_link,
                    headers={
                        "Sec-Fetch-Dest": "iframe",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "cross-site",
                        "Referer": "https://filemoon.sx/",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                        "Accept-Language": "en-GB,en;q=0.5",
                    },
                )
                r2.raise_for_status()

                with MoonM3u8Parser(r2.content.decode()) as p2:
                    if p2.m3u8_link:
                        main_url = p2.m3u8_link
                        break
            # print(main_url)
            if main_url is None:
                return None

            main_m3u8 = m3u8.load(main_url)
            if not main_m3u8.is_variant:
                return main_url, ""
            best_dimentions = 0
            best_resolution: str | None = None
            for playlist in main_m3u8.playlists:
                dim = playlist.stream_info.resolution
                assert dim
                dimentions = int(dim[0]) * int(dim[1])
                if dimentions > best_dimentions:
                    best_dimentions = dimentions
                    best_resolution = f"{dim[0]}x{dim[1]}"
            if best_resolution is None:
                return None
            return main_url, best_resolution
    except httpx.TimeoutException:
        return None
    except httpx.NetworkError:
        return None
    except httpx.ProtocolError:
        return None


def get_episodes_download_links(
    client: httpx.Client, links: dict[str, str]
) -> dict[str, tuple[str, str]]:
    res: dict[str, tuple[str, str]] = {}
    for ep in links:
        link = get_episode_download_link(client, links, ep)
        if link is not None:
            res[ep] = link
    return res


def get_episode_links(client: httpx.Client, anime_id: str) -> dict[str, str] | None:
    try:
        r = client.get(f"https://{animenosub_domain}/anime/{anime_id}")
        with EpListParser(r.content.decode()) as p:
            r.raise_for_status()
            return p.links
    except httpx.TimeoutException:
        return None
    except httpx.NetworkError:
        return None
    except httpx.ProtocolError:
        return None


def get_episodes_to_download(
    client: httpx.Client,
    anime_id: str,
    blacklist: list[str] | None,
    whitelist: list[str] | None,
) -> tuple[dict[str, str], dict[str, tuple[str, str]]] | tuple[None, None]:
    links = get_episode_links(client, anime_id)
    if links is None:
        return None, None
    links_to_download = links.copy()

    if blacklist is not None:
        links_to_download = blacklist_episode_links(links_to_download, blacklist)
    if whitelist is not None:
        links_to_download = whitelist_episode_links(links_to_download, whitelist)

    return links, get_episodes_download_links(client, links_to_download)


def episode_order(ep: str) -> float:
    for i in range(1, len(ep)):
        try:
            float(ep[:i])
        except ValueError:
            return float("0" + ep[: (i - 1)]) + 0.05
    return float("0" + ep)


def blacklist_episode_links(
    links: dict[str, str], blacklist: list[str]
) -> dict[str, str]:
    new_links: dict[str, str] = {}
    for i in links:
        if i not in blacklist:
            new_links[i] = links[i]
    return new_links


def whitelist_episode_links(
    links: dict[str, str], whitelist: list[str]
) -> dict[str, str]:
    new_links: dict[str, str] = {}
    for i in whitelist:
        if i in links:
            new_links[i] = links[i]
    return new_links
