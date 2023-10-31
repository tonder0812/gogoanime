import os

if os.name == "nt":
    import ctypes
    from ctypes import byref
    from ctypes.wintypes import DWORD
    from subprocess import STD_INPUT_HANDLE

    from .common import Key, Mouse, MouseType
    from .utils import length, remove_control_chars, split_lines_width
    from .windows_api import (
        DISABLE_NEWLINE_AUTO_RETURN,
        ENABLE_EXTENDED_FLAGS,
        ENABLE_MOUSE_INPUT,
        ENABLE_PROCESSED_INPUT,
        ENABLE_QUICK_EDIT_MODE,
        ENABLE_VIRTUAL_TERMINAL_PROCESSING,
        ENABLE_WINDOW_INPUT,
        disable_scroll,
        enable_scroll,
        get_console_mode,
        kernel,
        set_console_mode,
    )
    from .windows_events import (
        CAPSLOCK_ON,
        DOUBLE_CLICK,
        ENHANCED_KEY,
        FOCUS_EVENT,
        INPUT_RECORD,
        KEY_EVENT,
        LEFT_ALT_PRESSED,
        LEFT_CTRL_PRESSED,
        MENU_EVENT,
        MOUSE_EVENT,
        MOUSE_HWHEELED,
        MOUSE_MOVED,
        MOUSE_WHEELED,
        NUMLOCK_ON,
        RIGHT_ALT_PRESSED,
        RIGHT_CTRL_PRESSED,
        SCROLLLOCK_ON,
        SHIFT_PRESSED,
        WINDOW_BUFFER_SIZE_EVENT,
    )
    from .windows_vk import get_key_count, get_name, process_key_event

    def execute_ansii_escape_sequence(sequence: str):
        print("\033" + sequence, end="", flush=True)

    def move_cursor(y: int, x: int):
        execute_ansii_escape_sequence("[%d;%dH" % (y, x))

    def hide_cursor():
        execute_ansii_escape_sequence("[?25l")

    def show_cursor():
        execute_ansii_escape_sequence("[?25h")

    def clear_screen():
        move_cursor(1, 1)
        execute_ansii_escape_sequence("[J")

    def init() -> None:
        global original_out_mode, original_in_mode, new_out_mode, new_in_mode

        original_out_mode = get_console_mode(True)
        original_in_mode = get_console_mode(False)
        disable_scroll()
        requested_out_mode = (
            ENABLE_VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN
        )
        requested_in_modes = (  # ENABLE_VIRTUAL_TERMINAL_INPUT |
            ENABLE_PROCESSED_INPUT
            | ENABLE_EXTENDED_FLAGS
            | ENABLE_WINDOW_INPUT
            | ENABLE_MOUSE_INPUT
        )

        new_out_mode = original_out_mode | requested_out_mode
        new_in_mode = (original_in_mode | requested_in_modes) & ~ENABLE_QUICK_EDIT_MODE

        set_console_mode(new_out_mode, True)
        set_console_mode(new_in_mode, False)
        execute_ansii_escape_sequence("[?1049h")
        hide_cursor()
        clear_screen()

    def stop():
        execute_ansii_escape_sequence("[?1049l")
        enable_scroll()
        set_console_mode(original_out_mode, True)
        set_console_mode(original_in_mode, False)

    focus = True

    def is_focused() -> bool:
        return focus

    def poll_events() -> Key | Mouse | None:
        global terminal_size, focus
        set_console_mode(new_out_mode, True)
        set_console_mode(new_in_mode, False)
        save_ip = INPUT_RECORD()
        count = DWORD()

        hCon = kernel.GetStdHandle(STD_INPUT_HANDLE)
        kernel.GetNumberOfConsoleInputEvents(hCon, byref(count))
        if count.value == 0:
            return None
        kernel.ReadConsoleInputW(hCon, byref(save_ip), 1, byref(count))
        if save_ip.EventType == MENU_EVENT:
            return poll_events()

        if save_ip.EventType == WINDOW_BUFFER_SIZE_EVENT:
            terminal_size = (
                save_ip.Event.WindowBufferSizeEvent.dwSize.Y,
                save_ip.Event.WindowBufferSizeEvent.dwSize.X,
            )
            return poll_events()
        if save_ip.EventType == FOCUS_EVENT:
            focus = save_ip.Event.FocusEvent.bSetFocus
            return poll_events()
        if save_ip.EventType == KEY_EVENT:
            event = save_ip.Event.KeyEvent
            count = get_key_count(event)
            key = process_key_event(event)
            if key == -1:
                return poll_events()
            char = event.uChar.UnicodeChar
            if char == "\r":
                char = "\n"
            return Key(
                char=char,
                code=get_name(key),
                pressed=event.bKeyDown,
                repeat_count=count,
                capslock=event.dwControlKeyState & CAPSLOCK_ON != 0,
                enhanced=event.dwControlKeyState & ENHANCED_KEY != 0,
                left_alt=event.dwControlKeyState & LEFT_ALT_PRESSED != 0,
                left_ctrl=event.dwControlKeyState & LEFT_CTRL_PRESSED != 0,
                numlock=event.dwControlKeyState & NUMLOCK_ON != 0,
                right_alt=event.dwControlKeyState & RIGHT_ALT_PRESSED != 0,
                right_ctrl=event.dwControlKeyState & RIGHT_CTRL_PRESSED != 0,
                scrolllock=event.dwControlKeyState & SCROLLLOCK_ON != 0,
                shift=event.dwControlKeyState & SHIFT_PRESSED != 0,
            )
        if save_ip.EventType == MOUSE_EVENT:
            event = save_ip.Event.MouseEvent
            type_ = MouseType.PRESSED_CHANGE
            buttons = [
                i + 1 for i in range(32) if (event.dwButtonState & (1 << i)) != 0
            ]
            scroll = (0, 0)
            if event.dwEventFlags == MOUSE_WHEELED:
                scroll = (0, ctypes.c_int16(event.dwButtonState >> 16).value / 120)
                buttons = []
                type_ = MouseType.SCROLL
            if event.dwEventFlags == MOUSE_HWHEELED:
                scroll = (ctypes.c_int16(event.dwButtonState >> 16).value / 120, 0)
                buttons = []
                type_ = MouseType.SCROLL
            if event.dwEventFlags == MOUSE_MOVED:
                type_ = MouseType.MOVE
            if event.dwEventFlags == DOUBLE_CLICK:
                type_ = MouseType.DOUBLE_CLICK

            return Mouse(
                position=(event.dwMousePosition.X, event.dwMousePosition.Y),
                buttons=buttons,
                scroll=scroll,
                type_=type_,
                capslock=event.dwControlKeyState & CAPSLOCK_ON != 0,
                enhanced=event.dwControlKeyState & ENHANCED_KEY != 0,
                left_alt=event.dwControlKeyState & LEFT_ALT_PRESSED != 0,
                left_ctrl=event.dwControlKeyState & LEFT_CTRL_PRESSED != 0,
                numlock=event.dwControlKeyState & NUMLOCK_ON != 0,
                right_alt=event.dwControlKeyState & RIGHT_ALT_PRESSED != 0,
                right_ctrl=event.dwControlKeyState & RIGHT_CTRL_PRESSED != 0,
                scrolllock=event.dwControlKeyState & SCROLLLOCK_ON != 0,
                shift=event.dwControlKeyState & SHIFT_PRESSED != 0,
            )
        assert False, "UNREACHABLE"

    terminal_size = os.get_terminal_size().lines, os.get_terminal_size().columns

    def get_size() -> tuple[int, int]:
        return terminal_size

    def set_text(text: str, start: int = 0, should_set_cursor: bool = False):
        rows, cols = get_size()
        last_cursor = 1, 1
        move_cursor(1, 1)
        i = 0
        msg = ""
        for line in split_lines_width(remove_control_chars(text), cols, rows, start):
            msg += line + " " * (cols - length(line))
            last_cursor = i + 1, length(line) + 1
            i += 1
        for line in range(i, rows - 1):
            msg += " " * cols
        print(msg, end="", flush=True)
        if should_set_cursor:
            move_cursor(*last_cursor)
        else:
            move_cursor(1, 1)
