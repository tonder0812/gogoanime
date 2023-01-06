from typing import Any


def debug_log(message: Any, level: int = 0):
    if level >= 0:
        with open("debug.log", "a", encoding="utf-8") as _debugF:
            print(str(message).strip(), file=_debugF, flush=True)
