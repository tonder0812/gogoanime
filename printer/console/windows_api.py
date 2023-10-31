import os

if os.name == "nt":
    import ctypes
    from ctypes import wintypes
    from subprocess import STD_INPUT_HANDLE, STD_OUTPUT_HANDLE
    from typing import Any

    kernel = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    # input flags
    ENABLE_PROCESSED_INPUT = 0x0001
    ENABLE_LINE_INPUT = 0x0002
    ENABLE_ECHO_INPUT = 0x0004
    ENABLE_WINDOW_INPUT = 0x0008
    ENABLE_MOUSE_INPUT = 0x0010
    ENABLE_INSERT_MODE = 0x0020
    ENABLE_QUICK_EDIT_MODE = 0x0040
    ENABLE_EXTENDED_FLAGS = 0x0080
    ENABLE_VIRTUAL_TERMINAL_INPUT = 0x0200
    # output flags
    ENABLE_PROCESSED_OUTPUT = 0x0001
    ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004  # VT100 (Win 10)
    DISABLE_NEWLINE_AUTO_RETURN = 0x0008

    def check_zero(result: Any, func: Any, args: Any) -> Any:
        if not result:
            err = ctypes.get_last_error()
            if err:
                raise ctypes.WinError(err)
        return args

    if not hasattr(wintypes, "LPDWORD"):  # PY2
        wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

    kernel.GetConsoleMode.errcheck = check_zero
    kernel.GetConsoleMode.argtypes = (
        wintypes.HANDLE,  # _In_  hConsoleHandle
        wintypes.LPDWORD,  # _Out_ lpMode
    )

    kernel.SetConsoleMode.errcheck = check_zero
    kernel.SetConsoleMode.argtypes = (
        wintypes.HANDLE,  # _In_  hConsoleHandle
        wintypes.DWORD,  # _Out_ lpMode
    )

    def disable_scroll():
        user32.ShowScrollBar(kernel.GetConsoleWindow(), 1, 0)

    def enable_scroll():
        user32.ShowScrollBar(kernel.GetConsoleWindow(), 1, 1)

    def get_console_mode(output: bool = False) -> int:
        """Get the mode of the active console input or output
        buffer. Note that if the process isn't attached to a
        console, this function raises an EBADF IOError.
        """
        mode = wintypes.DWORD()
        if output:
            hCon = kernel.GetStdHandle(STD_OUTPUT_HANDLE)
        else:
            hCon = kernel.GetStdHandle(STD_INPUT_HANDLE)
        kernel.GetConsoleMode(hCon, ctypes.byref(mode))
        return mode.value

    def set_console_mode(mode: int, output: bool = False):
        """Set the mode of the active console input or output
        buffer. Note that if the process isn't attached to a
        console, this function raises an EBADF IOError.
        """
        if output:
            hCon = kernel.GetStdHandle(STD_OUTPUT_HANDLE)
        else:
            hCon = kernel.GetStdHandle(STD_INPUT_HANDLE)
        kernel.SetConsoleMode(hCon, mode)
