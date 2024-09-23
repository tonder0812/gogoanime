from http.cookiejar import CookieJar
import re
import urllib
from typing import Protocol
import urllib.parse

import browser_cookie3
import httpx

from config import browser, cookies_location, gogoanime_domain, email, password


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
    if email is not None and password is not None:
        s = httpx.Client()
        r = s.get(f"https://{gogoanime_domain}/login.html")
        content = r.content.decode()
        csrf = re.findall(r"_csrf'\s+value='(\w+)'", content)[0]
        print(csrf, s.cookies)
        r = s.post(
            f"https://{gogoanime_domain}/login.html",
            content=urllib.parse.urlencode(
                {"_csrf": csrf, "email": email, "password": password}
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            follow_redirects=False,
        )
        return s.cookies.jar
    if browser is None:
        return CookieJar()
    return loaders[browser](cookie_file=cookies_location, domain_name=gogoanime_domain)
