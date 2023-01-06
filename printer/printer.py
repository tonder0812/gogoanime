import os
import threading
import time
from threading import Thread
from typing import Any, Callable, Generator, Optional, Self

from pynput import keyboard
from urwid.util import str_util

if __name__ == "__main__":
    from console import (ENABLE_EXTENDED_FLAGS, ENABLE_QUICK_EDIT_MODE,
                         is_focused, update_console_mode)
    from fakePrinter import FakePrinter
else:
    from printer.console import (ENABLE_EXTENDED_FLAGS, ENABLE_QUICK_EDIT_MODE,
                                 is_focused, update_console_mode)
    from printer.fakePrinter import FakePrinter


def execute_ansii_escape_sequence(sequence: str):
    print("\033["+sequence, end="", flush=True)


def move_cursor(y: int, x: int):
    execute_ansii_escape_sequence("%d;%dH" % (y, x))


def clear_screen():
    move_cursor(0, 0)
    execute_ansii_escape_sequence("J")


def length(text: str) -> int:
    total: int = 0
    for c in text:
        total += str_util.get_width(ord(c))
    return total


def cut_unicode(text: str, width: int) -> tuple[str, str]:
    res: str = ""
    res_len: int = 0
    safe = text
    for c in safe:
        res_len += str_util.get_width(ord(c))
        if (res_len > width):
            break
        res += c
        text = text[1:]
    return res, text


def calc_rows(text: str, width: int) -> int:
    current = 0
    for line in text.split("\n"):
        while length(line) >= width:
            current += 1
            _, line = cut_unicode(line, width)
        current += 1
    return current


def split_lines_width(text: str, width: int, height: int, start: int) -> Generator[str, None, None]:
    current = 0
    for line in text.split("\n"):
        while length(line) >= width:
            current += 1
            s, line = cut_unicode(line, width)
            if current > start:
                if current-start >= height:
                    return
                yield s
        current += 1
        if current > start:
            if current-start >= height:
                return
            yield line


class Printer:
    _instance: Optional["Printer"] = None
    _lock: threading.Lock = threading.Lock()
    _initialised: bool = False
    data: dict[str, Any] = {}
    desc: str = ""
    msg: str = ""
    renderThread: Thread
    stopped: bool = False
    waiting: bool = False
    delay: float = 0.1
    start: int = 0
    height: int = 0
    width: int = 0

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
        os.system("cls")
        clear_screen()
        event_filter: Callable[[Any, Any], Any] = lambda _, __: is_focused()
        self.listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release,
            win32_event_filter=event_filter)
        self.listener.start()
        self.renderThread = Thread(target=self.render)
        self.renderThread.start()
        update_console_mode(ENABLE_EXTENDED_FLAGS,
                            ENABLE_QUICK_EDIT_MODE | ENABLE_EXTENDED_FLAGS)

    def wait(self) -> Self:
        with self._lock:
            self.__render(False)
            self.waiting = True
        return self

    def format_msg(self) -> None:
        self.msg = self.desc.format(**self.data)

    def resume(self) -> Self:
        with self._lock:
            self.__render()
            self.waiting = False
        return self

    def input(self, question: str = "") -> str:
        self.print(question, end="")
        last = calc_rows(self.msg, self.width)
        if self.start <= last and (self.start + self.height) >= last:
            pass
        else:
            self.start += last - (self.start + self.height - 3)
        self.start = self.start if self.start > 0 else 0
        self.wait()
        out = input("")
        self.print(out)
        self.resume()
        return out

    def stop(self) -> Self:
        with self._lock:
            self.stopped = True

        self.listener.stop()

        self.renderThread.join()
        self.listener.join()
        print(self.msg)
        return self

    def render(self) -> None:
        while True:
            with self._lock:
                if not self.waiting:
                    self.__render()
                if self.stopped:
                    return
            time.sleep(self.delay)

    def __render(self, should_move_cursor: bool = True) -> None:
        # Get Terminal size
        size = os.get_terminal_size()
        self.height = size.lines
        self.width = size.columns
        # Clamp cursor
        self.start = self.start if self.start > 0 else 0
        # clear screen
        # clear_screen()
        # Render message
        move_cursor(0, 1)
        i = 1
        last_cursor = 0, 0
        msg = ""
        for line in split_lines_width(self.msg, self.width, self.height-1, self.start):
            msg += line+" "*(self.width-length(line))
            last_cursor = i, length(line)+1
            i += 1
        for line in range(i, self.height):
            msg += " "*(self.width)
        print(msg, end="", flush=True)
        move_cursor(*last_cursor)
        if should_move_cursor:
            move_cursor(0, 0)

    def set_delay(self, delay: float) -> Self:
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
            self.format_msg()
        return self

    def set(self, name: str, data: Any) -> Self:
        with self._lock:
            self.data[name] = data
            self.format_msg()
        return self

    def get(self, name: str) -> Any:
        with self._lock:
            data = self.data.get(name)
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

    def __on_press(self, key: keyboard.Key | keyboard.KeyCode | None):
        if key is None:
            return

        if self.waiting:
            return

        if isinstance(key, keyboard.Key):
            if key == keyboard.Key.up:
                with self._lock:
                    self.start -= 1
            elif key == keyboard.Key.down:
                with self._lock:
                    self.start += 1

    def __on_release(self, key: keyboard.Key | keyboard.KeyCode | None):
        if key is None:
            return


PrinterType = Printer | FakePrinter


def main():
    p = Printer()
    p.print("😊1😊2😊3😊4😊5😊6😊7😊8😊9😊0\naa\n")
    p.print(cut_unicode("😊a😊b", 3))
    try:
        for i in range(100):
            p.print(i)
            # if (i % 5 == 0):
            #     p.print(p.input("test "))
            time.sleep(1)
    except:
        pass
    finally:
        p.stop()
        os.system("title finish")


if __name__ == '__main__':
    main()
