class Segment:
    absolute_uri: str


class M3U8:
    segments: list[Segment]


def load(uri: str, headers: dict[str, str | bytes] | None) -> M3U8:
    ...
