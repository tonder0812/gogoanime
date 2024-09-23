import unicodedata


def digits(x: int):
    return len(str(x))


def generate_anime_logo_filename(
    logo_format: str, anime_name: str, anime_id: str
) -> str:
    return logo_format.format(title=anime_name, id=anime_id) + ".png"


def generate_anime_dirname(folder_format: str, anime_name: str, anime_id: str) -> str:
    return folder_format.format(title=anime_name, id=anime_id)


def generate_episode_filename_and_description(
    episode_format: str,
    eps: list[str],
    episode_number: int,
    ep: str,
    anime_name: str,
    anime_id: str,
) -> tuple[str, str]:
    index = str(episode_number).rjust(max(digits(len(eps)), 2), "0")
    desc = episode_format.format(index=index, name=ep, title=anime_name, id=anime_id)
    return (desc + ".mp4", desc)


def format_time(time: float) -> str:
    hours, rem = divmod(time, 3600)
    minutes, seconds = divmod(rem, 60)
    if hours == 0:
        return "{:0>2}m:{:05.2f}s".format(int(minutes), seconds)
    return "{:0>2}h:{:0>2}m:{:05.2f}s".format(int(hours), int(minutes), seconds)


def delta_time_str(start: float, end: float) -> str:
    return format_time(end - start)


# String formating


def normalize_filename(string: str, is_directory: bool = True) -> str:
    string = (
        unicodedata.normalize("NFKD", string.strip())
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )
    validchars = "-_.()! "
    if is_directory:
        validchars += "\\/:"
    out = ""
    for c in string:
        if str.isalpha(c) or str.isdigit(c) or (c in validchars):
            out += c
        else:
            out += "_"
    while out[-1] == ".":
        out = out[:-1]
    return out
