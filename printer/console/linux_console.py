
from .console import Key, Mouse


def move_cursor(y: int, x: int):
    assert False, "LINUX UNINPLEMENTED"


def hide_cursor():
    assert False, "LINUX UNINPLEMENTED"


def show_cursor():
    assert False, "LINUX UNINPLEMENTED"


def clear_screen():
    assert False, "LINUX UNINPLEMENTED"


def init() -> None:
    assert False, "LINUX UNINPLEMENTED"


def stop():
    assert False, "LINUX UNINPLEMENTED"


def is_focused() -> bool:
    assert False, "LINUX UNINPLEMENTED"


def poll_events() -> Key | Mouse | None:
    assert False, "LINUX UNINPLEMENTED"


def get_size() -> tuple[int, int]:
    assert False, "LINUX UNINPLEMENTED"


def set_text(text: str, start: int = 0, should_set_cursor: bool = False):
    assert False, "LINUX UNINPLEMENTED"
