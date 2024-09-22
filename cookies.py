from http.cookiejar import CookieJar
from typing import Protocol

import browser_cookie3

from config import browser, cookies_location, gogoanime_domain


class CookieLoader(Protocol):
    @staticmethod
    def __call__(
        cookie_file: str | None = ...,
        domain_name: str | None = ...,
    ) -> CookieJar: ...


loaders: dict[str, CookieLoader] = {
    "chrome": browser_cookie3.chrome,
    "chromium": browser_cookie3.chromium,
    "opera": browser_cookie3.opera,
    "brave": browser_cookie3.brave,
    "edge": browser_cookie3.edge,
    "vivaldi": browser_cookie3.vivaldi,
    "firefox": browser_cookie3.firefox,
    "safari": browser_cookie3.safari,
}


def load_cookies() -> CookieJar:
    if browser is None:
        return CookieJar()
    return loaders[browser](cookie_file=cookies_location, domain_name=gogoanime_domain)
