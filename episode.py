import requests

from parsers import EpListParser, VideoLinkParser


def get_episode_download_link(session: requests.Session, links: dict[str, str], episode: str) -> str | None:
    try:
        with (
            session.get(f"https://gogoanime.tel{links[episode]}") as r,
            VideoLinkParser(r.content.decode()) as p
        ):
            r.raise_for_status()
            return p.downloadLink
    except requests.exceptions.ConnectionError:
        return None


def get_episodes_download_links(session: requests.Session, links: dict[str, str]) -> dict[str, str]:
    res: dict[str, str] = {}
    for ep in links:
        link = get_episode_download_link(session, links, ep)
        if link is not None:
            res[ep] = link
    return res


def get_episode_links(session: requests.Session, anime_id: str) -> dict[str, str] | None:
    try:
        with (
            session.get(f"https://ajax.gogo-load.com/ajax/load-list-episode?id={anime_id}&ep_start=0&ep_end=100000") as r,
            EpListParser(r.content.decode()) as p
        ):
            r.raise_for_status()
            return p.links
    except requests.exceptions.ConnectionError:
        return None


def get_episodes_to_download(session: requests.Session, anime_id: str, already_downloaded: list[str]) -> tuple[dict[str, str], dict[str, str]] | tuple[None, None]:
    links = get_episode_links(session, anime_id)
    if links is None:
        return None, None
    links_to_download = links.copy()
    filter_blacklist_episode_links(links_to_download, already_downloaded)

    return links, get_episodes_download_links(session, links_to_download)


def episode_order(ep: str) -> float:
    for i in range(1, len(ep)):
        try:
            float(ep[:i])
        except ValueError:
            return float("0" + ep[:(i - 1)]) + 0.05
    return float("0" + ep)


def filter_blacklist_episode_links(links: dict[str, str], blacklist: list[str]):
    for i in blacklist:
        if i in links:
            del links[i]
