import threading
from typing import Any, Optional, Self


class FakePrinter:
    _instance: Optional["FakePrinter"] = None
    _lock: threading.Lock = threading.Lock()
    _initialised: bool = False
    data: dict[str, Any] = {}
    desc: str = ""
    stopped: bool = False
    waiting: bool = False
    delay: float = 0.1
    terminal: bool = False

    def __new__(cls, *args: Any, **kwargs: Any):
        with cls._lock:
            if not cls._instance:
                cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # instance has already been created
        if self._initialised:
            return
        self._initialised = True

    def wait(self) -> Self:
        with self._lock:
            self.waiting = True
        return self

    def resume(self) -> Self:
        with self._lock:
            self.waiting = False
        return self

    def input(self, question: str = "") -> str:
        self.print(question, end="")
        self.wait()
        out = input("")
        self.print(out)
        self.resume()
        return out

    def stop(self) -> Self:
        with self._lock:
            self.stopped = True
        return self

    def setDelay(self, delay: float) -> Self:
        with self._lock:
            self.delay = delay
        return self

    def print(self, *args: Any, sep: str = " ", end: str = "\n", escape: bool = True) -> Self:
        arg = sep.join(map(str, args))
        if escape:
            arg = arg.replace("{", "{{").replace("}", "}}")
            end = end.replace("{", "{{").replace("}", "}}")
        with self._lock:
            self.desc += arg + end
        return self

    def set(self, name: str, data: Any) -> Self:
        with self._lock:
            self.data[name] = data
        return self

    def get(self, name: str) -> Any:
        with self._lock:
            data = self.data.get(name)
            return data

    def set_desc(self, *args: Any, sep: str = " ") -> Self:
        desc = sep.join(map(str, args))
        with self._lock:
            self.desc = desc
        return self

    def add_desc(self, *args: Any, sep: str = " ") -> Self:
        desc = sep.join(map(str, args))
        with self._lock:
            self.desc += desc
        return self

    def get_desc(self) -> str:
        with self._lock:
            return self.desc
