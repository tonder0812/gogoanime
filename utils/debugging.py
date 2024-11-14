from typing import Any

log_level: int = 0


def set_log_level(level: int):
    global log_level
    log_level = level


def debug_log(message: Any, level: int = 0):
    if level <= log_level:
        with open("debug.log", "a", encoding="utf-8") as _debugF:
            print(str(message).strip(), file=_debugF, flush=True)
