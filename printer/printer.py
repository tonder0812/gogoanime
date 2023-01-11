import threading
import time
from threading import Thread
from typing import Any, Self

from printer.scroller import Scroller


from .console import console
from .console.utils import calc_rows, remove_control_chars


class Printer:
    _lock: threading.RLock = threading.RLock()
    data: dict[str, Any] = {}
    desc: str = ""
    msg: str = ""
    renderThread: Thread
    stopped: bool = False
    waiting: bool = False
    delay: float = 0
    height: int = 0
    width: int = 0

    scroller = Scroller()

    def __init__(self):
        console.init()
        self.renderThread = Thread(target=self.render)
        self.renderThread.start()

    def wait(self) -> Self:
        with self._lock:
            self.__render(True)
            self.waiting = True
        return self

    def format_msg(self) -> None:
        with self._lock:
            self.msg = self.desc.format(**self.data)

    def resume(self) -> Self:
        with self._lock:
            self.waiting = False
            self.__render()
        return self

    def input(self, question: str = "") -> str:
        with self._lock:
            self.print(question, end="")

            start = int(self.scroller.position)
            last = calc_rows(self.msg, self.width)
            end = start + self.height
            if start > last or end < last:
                start = last - self.height + 3

            self.scroller.position = start
            self.scroller.velocity = 0
            self.wait()

            console.show_cursor()
            out = input()
            console.hide_cursor()

            self.print(out)
            self.resume()
        return out

    def stop(self) -> Self:
        with self._lock:
            self.stopped = True

        self.renderThread.join()
        console.stop()
        print(remove_control_chars(self.msg))
        return self

    def render(self) -> None:
        while True:
            with self._lock:
                if not self.waiting:
                    self.__render()
                if self.stopped:
                    return
            time.sleep(self.delay)

    def __render(self, should_set_cursor: bool = False) -> None:
        with self._lock:
            velocity = 0
            while (event := console.poll_events()) is not None:
                if isinstance(event, console.Key):
                    if not event.pressed:
                        continue
                    if event.code == "KEY_UP":
                        self.scroller.position -= 1
                        self.scroller.velocity = 0
                    elif event.code == "KEY_DOWN":
                        self.scroller.position += 1
                        self.scroller.velocity = 0
                else:
                    if event.scroll[1] != 0 and abs(event.scroll[1] % 120) == 0:
                        self.scroller.position -= event.scroll[1]/120
                        self.scroller.velocity = 0
                    else:
                        velocity -= event.scroll[1]
            # Get Terminal size
            self.height, self.width = console.get_size()
            rows = calc_rows(self.msg, self.width)-2
            self.scroller.update(
                1.25*velocity/120, rows)
            # Render message
            console.set_text(self.msg, int(
                self.scroller.position), should_set_cursor)

    def set_delay(self, delay: float) -> Self:
        with self._lock:
            self.delay = delay
        return self

    def print(self, *args: Any, sep: str = " ", end: str = "\n", escape: bool = True) -> Self:
        with self._lock:
            arg = sep.join(map(str, args))
            if escape:
                arg = arg.replace("{", "{{").replace("}", "}}")
                end = end.replace("{", "{{").replace("}", "}}")
            self.desc += arg + end
            self.format_msg()
        return self

    def set(self, name: str, data: Any) -> Self:
        with self._lock:
            self.data[name] = data
            self.format_msg()
        return self

    def get(self, name: str, default: Any = None) -> Any:
        with self._lock:
            data = self.data.get(name, default)
            return data

    def set_desc(self, *args: Any, sep: str = " ") -> Self:
        desc = sep.join(map(str, args))
        with self._lock:
            self.desc = desc
            self.format_msg()
        return self

    def add_desc(self, *args: Any, sep: str = " ") -> Self:
        desc = sep.join(map(str, args))
        with self._lock:
            self.desc += desc
            self.format_msg()
        return self

    def get_desc(self) -> str:
        with self._lock:
            return self.desc
