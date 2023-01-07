import requests

from anime import get_anime_info
from cookies import load_cookies
from episode import (filter_blacklist_episode_links, get_episode_links,
                     get_episodes_download_links)


def main():
    s = requests.Session()
    s.cookies.update(load_cookies())
    info = get_anime_info(s, "mairimashita-iruma-kun-3rd-season")
    assert info is not None
    print(info.anime_id)
    print(info.name)
    print(info.logo_url)
    links = get_episode_links(s, info.anime_id)
    assert links is not None
    watched = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    filter_blacklist_episode_links(links, watched)
    print(get_episodes_download_links(s, links))


if __name__ == "__main__":
    main()
