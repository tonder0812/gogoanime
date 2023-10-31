import httpx

from config import gogoanime_domain
from parsers import AnimeParser


class AnimeInfo:
    def __init__(self, anime_id: str, name: str, logo_url: str | None) -> None:
        self.anime_id = anime_id
        self.name = name
        self.logo_url = logo_url


def get_anime_info(client: httpx.Client, anime_id: str) -> AnimeInfo | None:
    try:
        r = client.get(f"https://{gogoanime_domain}/category/{anime_id}")
        with AnimeParser(r.content.decode()) as p:
            r.raise_for_status()
            assert p.id is not None
            assert p.name is not None
            return AnimeInfo(p.id, p.name, p.logo_url)
    except httpx.TimeoutException:
        return None
    except httpx.NetworkError:
        return None
    except httpx.ProtocolError:
        return None
