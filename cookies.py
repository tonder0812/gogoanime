from http.cookiejar import CookieJar

import browser_cookie3

from config import browser, cookies_location, gogoanime_domain

loaders = {
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
