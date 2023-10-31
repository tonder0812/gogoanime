from abc import ABC, abstractmethod
from typing import Any, Self

from .prioritylock import PriorityRLock


class AbstractPrinter(ABC):
    def __init__(self) -> None:
        self._lock: PriorityRLock = PriorityRLock()
        self.data: dict[str, Any] = {}
        self.desc: str = ""
        self.msg: str = ""
        self.delay: float = 0.01
        self.formated: bool = True

    @abstractmethod
    def stop(self):
        ...

    @abstractmethod
    def input(self, question: str = "") -> str:
        ...

    def format_msg(self) -> None:
        with self._lock:
            self.formated = True
            self.msg = self.desc.format(**self.data)

    def set_delay(self, delay: float) -> Self:
        with self._lock:
            self.delay = delay
        return self

    def set(self, name: str, data: Any) -> Self:
        with self._lock:
            self.data[name] = data
            self.formated = False
        return self

    def get(self, name: str) -> Any:
        return self.data.get(name)

    def get_lock(self):
        return self._lock

    def set_desc(self, *args: Any, sep: str = " ") -> Self:
        desc = sep.join(map(str, args))
        with self._lock:
            self.desc = desc
            self.formated = False
        return self

    def add_desc(self, *args: Any, sep: str = " ") -> Self:
        desc = sep.join(map(str, args))
        with self._lock:
            self.desc += desc
            self.formated = False
        return self

    def get_desc(self) -> str:
        return self.desc

    def print(
        self, *args: Any, sep: str = " ", end: str = "\n", escape: bool = True
    ) -> Self:
        arg = sep.join(map(str, args))
        if escape:
            arg = arg.replace("{", "{{").replace("}", "}}")
            end = end.replace("{", "{{").replace("}", "}}")
        with self._lock:
            self.desc += arg + end
            self.formated = False
        return self
