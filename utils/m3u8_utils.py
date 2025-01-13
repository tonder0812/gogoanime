from pathlib import Path
from typing import Protocol, Sequence
from urllib.parse import urlparse
import m3u8


class HasUri(Protocol):
    uri: str | None


def replace_m3u8_uris(name: str, to_replace: Sequence[HasUri], tmp_dir: Path):
    tmp_files: list[Path] = []
    urls: list[str] = []
    for i, item in enumerate(to_replace, 1):
        assert item.uri is not None
        p = urlparse(item.uri).path
        assert isinstance(p, str)
        path = Path(p)
        extension = path.suffix
        tmp_file = tmp_dir / f"{name}{i}{extension}"
        tmp_files.append(tmp_file)
        urls.append(item.uri)
        item.uri = str(tmp_file).replace("\\", "/")
    return tmp_files, urls


def select_best_playlist(master: m3u8.M3U8):
    best_playlist = None
    best_resolution = 0
    for playlist in master.playlists:
        if playlist.stream_info.resolution:
            w, h = playlist.stream_info.resolution
            if w * h > best_resolution:
                best_resolution = w * h
                best_playlist = playlist
    assert best_playlist
    assert best_playlist.uri
    return best_playlist
