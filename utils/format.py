import unicodedata


def digits(x: int):
    return len(str(x))


def episode_filename_format(total_eps: int):
    return "{:0" + str(max(digits(total_eps), 2)) + "d}({}).mp4"


def episode_desc_format(total_eps: int, max_episode_length: int):
    return f"{{:0{str(max(digits(total_eps), 2))}d}}({{:<{str(max_episode_length)}}})"


def generate_filenames(eps: list[str], episode_number: int, ep: str) -> tuple[str, str]:
    max_episode_length = max(map(len, eps))
    return (
        episode_filename_format(len(eps)).format(episode_number, "episode-" + ep),
        episode_desc_format(len(eps), max_episode_length).format(
            episode_number, "episode-" + ep
        ),
    )


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
