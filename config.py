import json
from os import path
from pathlib import Path
from typing import Any

from utils import debugging
from utils.asyncio_downloader import DownloadTask

config_location = "./config"
new_location = path.join(config_location, "new.txt")
quit_location = path.join(config_location, "quit.txt")
watching_location = path.join(config_location, "watching.txt")
config_json_location = path.join(config_location, "config.json")

valid_browsers = (
    "chrome",
    "chromium",
    "opera",
    "brave",
    "edge",
    "vivaldi",
    "firefox",
    "safari",
)

with open(config_json_location, "r", encoding="utf-8") as f:
    options: dict[str, Any] = json.load(f)

download_path = Path(options.get("download_path", "./Downloads"))
if not download_path.exists() or not download_path.is_dir():
    print("Invalid config: download_path, must be a directory")
    exit(1)

episode_format = options.get("episode_format", "{index}(episode-{name})")
if not isinstance(episode_format, str):
    print("Invalid config: episode_format, must be a string")
    exit(1)

folder_format = options.get("folder_format", "{title}")
if not isinstance(folder_format, str):
    print("Invalid config: folder_format, must be a string")
    exit(1)

logo_format = options.get("logo_format", "logo")
if not isinstance(logo_format, str):
    print("Invalid config: logo_format, must be a string")
    exit(1)


notification_file_location = options.get("notification_file_location")
if notification_file_location is not None and not isinstance(
    notification_file_location, str
):
    print("Invalid config: notification_file_location, must be a string or null")
    exit(1)


browser = options.get("browser", "chrome")
if browser not in valid_browsers:
    print(f"Invalid config: browser, must be one of {','.join(valid_browsers)}")
    exit(1)
assert isinstance(browser, str)

email = options.get("email")
if email is not None and not isinstance(email, str):
    print(f"Invalid config: email, must be a string or null")
    exit(1)

password = options.get("password")
if password is not None and not isinstance(password, str):
    print(f"Invalid config: password, must be a string or null")
    exit(1)

cookies_location = options.get("cookies_location")
if cookies_location is None and (email is None or password is None):
    print(
        f"Invalid config: either email and password or cookies_location must be provided"
    )

if cookies_location is not None and not isinstance(cookies_location, str):
    print(f"Invalid config: cookies_location, must be a string or null")
    exit(1)

max_full_tries = options.get("max_full_tries", 50)
if not isinstance(max_full_tries, int) or (
    max_full_tries != -1 and max_full_tries <= 0
):
    print(f"Invalid config: max_full_tries, must be a positive integer or -1")
    exit(1)

max_inner_tries = options.get("max_inner_tries", 50)
if not isinstance(max_inner_tries, int) or (
    max_inner_tries != -1 and max_inner_tries <= 0
):
    print(f"Invalid config: max_inner_tries, must be a positive integer or -1")
    exit(1)

segments = options.get("segments", 10)
if not isinstance(segments, int) or (segments <= 0):
    print(f"Invalid config: segments, must be a positive integer")
    exit(1)

gogoanime_domain = options.get("gogoanime_domain", "gogoanime3.cc")
if not isinstance(gogoanime_domain, str):
    print("Invalid config: gogoanime_domain, must be a string")
    exit(1)

concurrent_downloads = options.get("concurrent_downloads", 6)
if not isinstance(concurrent_downloads, int) or (concurrent_downloads <= 0):
    print(f"Invalid config: concurrent_downloads, must be a positive integer")
    exit(1)

debug_mode = options.get("debug_mode", False)
if not isinstance(debug_mode, bool):
    print(f"Invalid config: debug_mode, must be true or false")

if debug_mode:
    debugging.set_log_level(1)
DownloadTask.set_max_concurrent_downloads(concurrent_downloads)


def user_end_download(filename: Path, success: bool, data: str):
    if success and notification_file_location is not None:
        with open(
            path.join(notification_file_location, "downloaded.txt"),
            "a",
            encoding="utf-8",
        ) as f:
            f.write(f"{data}\n")


def user_start_downloading(data: str):
    if notification_file_location is not None:
        with open(
            path.join(notification_file_location, "new.txt"), "a", encoding="utf-8"
        ) as f:
            f.write(f"{data}\n")
