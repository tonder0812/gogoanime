import time
from threading import Thread
from typing import Self, override
from printer.abstract_printer import AbstractPrinter

from printer.scroller import Scroller


from .console.utils import calc_rows, remove_control_chars
import printer.console as console


class Printer(AbstractPrinter):
    def __init__(self):
        super().__init__()

        self.stopped: bool = False
        self.waiting: bool = False
        self.height: int = 0
        self.width: int = 0
        self.scroller = Scroller()

        console.init()
        self.render_thread = Thread(target=self.render)
        self.render_thread.start()

    def wait(self) -> Self:
        with self._lock:
            self.__render(True)
            self.waiting = True
        return self

    def resume(self) -> Self:
        with self._lock:
            self.waiting = False
            self.__render()
        return self

    @override
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

    @override
    def stop(self):
        with self._lock:
            self.stopped = True

        self.render_thread.join()
        console.stop()
        print(remove_control_chars(self.msg))

    def render(self) -> None:
        while True:
            if not self.waiting:
                self.__render()

            if self.stopped:
                return
            time.sleep(self.delay)

    def __render(self, should_set_cursor: bool = False) -> None:
        with self._lock(-1):
            if not self.formated:
                self.format_msg()
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
                    if event.scroll[1] != 0 and abs(event.scroll[1] % 1) == 0:
                        self.scroller.position -= event.scroll[1]
                        self.scroller.velocity = 0
                    else:
                        velocity -= event.scroll[1]
            # Get Terminal size
            self.height, self.width = console.get_size()
            rows = calc_rows(self.msg, self.width) - 2
            self.scroller.update(1 * velocity, rows)
            # Render message
            console.set_text(self.msg, int(self.scroller.position), should_set_cursor)
