from typing import override
from .abstract_printer import AbstractPrinter


class FakePrinter(AbstractPrinter):
    def __init__(self):
        super().__init__()

    @override
    def input(self, question: str = "") -> str:
        self.print(question, end="")
        out = input("")
        self.print(out)
        return out

    @override
    def stop(self):
        return
