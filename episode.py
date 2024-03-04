import httpx

from config import gogoanime_domain
from parsers import EpListParser, VideoLinkParser


def get_episode_download_link(
    client: httpx.Client, links: dict[str, str], episode: str
) -> str | None:
    try:
        r = client.get(f"https://{gogoanime_domain}{links[episode]}")
        with VideoLinkParser(r.content.decode()) as p:
            r.raise_for_status()
            return p.download_link
    except httpx.TimeoutException:
        return None
    except httpx.NetworkError:
        return None
    except httpx.ProtocolError:
        return None


def get_episodes_download_links(
    client: httpx.Client, links: dict[str, str]
) -> dict[str, str]:
    res: dict[str, str] = {}
    for ep in links:
        link = get_episode_download_link(client, links, ep)
        if link is not None:
            res[ep] = link
    return res


def get_episode_links(client: httpx.Client, anime_id: str) -> dict[str, str] | None:
    try:
        r = client.get(
            f"https://ajax.gogocdn.net/ajax/load-list-episode?id={anime_id}&ep_start=0&ep_end=100000"
        )
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
) -> tuple[dict[str, str], dict[str, str]] | tuple[None, None]:
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
