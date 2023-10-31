import os

from .common import *

if os.name == "nt":
    from .windows_console import (
        clear_screen,
        get_size,
        hide_cursor,
        init,
        is_focused,
        move_cursor,
        poll_events,
        set_text,
        show_cursor,
        stop,
    )
else:
    from .linux_console import (
        clear_screen,
        get_size,
        hide_cursor,
        init,
        is_focused,
        move_cursor,
        poll_events,
        set_text,
        show_cursor,
        stop,
    )
__all__ = [
    "Key",
    "Mouse",
    "MouseType",
    "clear_screen",
    "poll_events",
    "get_size",
    "hide_cursor",
    "init",
    "is_focused",
    "move_cursor",
    "set_text",
    "show_cursor",
    "stop",
]
