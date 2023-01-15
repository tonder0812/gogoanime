from .abstract_printer import AbstractPrinter
from .fake_printer import FakePrinter as _FakePrinter
from .printer import Printer as _Printer

__all__ = ["Printer", "FakePrinter", "AbstractPrinter"]
_printer: _Printer | None = None
_fake_printer: _FakePrinter | None = None


def Printer() -> _Printer:
    global _printer
    if _printer is None:
        _printer = _Printer()
    return _printer


def FakePrinter() -> _FakePrinter:
    global _fake_printer
    if _fake_printer is None:
        _fake_printer = _FakePrinter()
    return _fake_printer
