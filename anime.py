import requests

from parsers import AnimeParser


class AnimeInfo:
    def __init__(self, anime_id: str, name: str, logo_url: str | None) -> None:
        self.anime_id = anime_id
        self.name = name
        self.logo_url = logo_url


def get_anime_info(session: requests.Session, anime_link: str) -> AnimeInfo | None:
    try:
        with (
            session.get(f"https://gogoanime.tel/category/{anime_link}") as r,
            AnimeParser(r.content.decode()) as p
        ):
            r.raise_for_status()
            assert p.id is not None
            assert p.name is not None
            return AnimeInfo(p.id, p.name, p.logo_url)
    except requests.exceptions.ConnectionError:
        return None
