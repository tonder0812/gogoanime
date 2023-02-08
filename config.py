import json
from os import path
from typing import Any, Optional

max_tries = 50

config_location = "./config"
new_location = path.join(config_location, "new.txt")
quit_location = path.join(config_location, "quit.txt")
watching_location = path.join(config_location, "watching.txt")
config_json_location = path.join(config_location, "config.json")

download_path: str = "./Downloads"
notification_file_location: Optional[str] = None
browser: str | None = "chrome"
cookies_location: str | None = None

with open(config_json_location, "r") as f:
    options = json.load(f)
download_path = options.get("download_path", download_path)
notification_file_location = options.get(
    "notification_file_location", notification_file_location)
browser = options.get("browser", notification_file_location)
cookies_location = options.get(
    "cookies_location", notification_file_location)


def user_end_download(filename: str, success: bool, data: Any):
    if success and notification_file_location is not None:
        with open(path.join(notification_file_location, "downloaded.txt"), "a", encoding="utf-8") as f:
            f.write(f"{data}\n")


def user_start_downloading(showName: str, ep: str):
    if notification_file_location is not None:
        with open(path.join(notification_file_location, "new.txt"), "a", encoding="utf-8") as f:
            f.write(f"{showName} - {ep}\n")
