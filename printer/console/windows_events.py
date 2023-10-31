import os

if os.name == "nt":
    from ctypes import Structure, Union, c_byte, c_char, c_int, c_short, c_wchar
    from ctypes.wintypes import BOOL, DWORD, SHORT, UINT, WORD

    CAPSLOCK_ON = 0x0080
    ENHANCED_KEY = 0x0100
    LEFT_ALT_PRESSED = 0x0002
    LEFT_CTRL_PRESSED = 0x0008
    NUMLOCK_ON = 0x0020
    RIGHT_ALT_PRESSED = 0x0001
    RIGHT_CTRL_PRESSED = 0x0004
    SCROLLLOCK_ON = 0x0040
    SHIFT_PRESSED = 0x0010

    FROM_LEFT_1ST_BUTTON_PRESSED = 0x0001
    FROM_LEFT_2ND_BUTTON_PRESSED = 0x0004
    FROM_LEFT_3RD_BUTTON_PRESSED = 0x0008
    FROM_LEFT_4TH_BUTTON_PRESSED = 0x0010
    RIGHTMOST_BUTTON_PRESSED = 0x0002

    DOUBLE_CLICK = 0x0002
    MOUSE_HWHEELED = 0x0008
    MOUSE_MOVED = 0x0001
    MOUSE_WHEELED = 0x0004

    def modifiers(mod: int) -> str:
        res = ""
        if mod & CAPSLOCK_ON != 0:
            res += "CapsLock,"
        if mod & ENHANCED_KEY != 0:
            res += "Enhance,"
        if mod & LEFT_ALT_PRESSED != 0:
            res += "LeftAlt,"
        if mod & LEFT_CTRL_PRESSED != 0:
            res += "LeftCtrl,"
        if mod & NUMLOCK_ON != 0:
            res += "NumLock,"
        if mod & RIGHT_ALT_PRESSED != 0:
            res += "RighttAlt,"
        if mod & RIGHT_CTRL_PRESSED != 0:
            res += "RightCtrl,"
        if mod & SCROLLLOCK_ON != 0:
            res += "ScrollLock,"
        if mod & SHIFT_PRESSED != 0:
            res += "Shift,"

        if len(res) > 0:
            res = res[:-1]
        return res

    def mouse_keys(key: int) -> str:
        res = ""
        if key & FROM_LEFT_1ST_BUTTON_PRESSED:
            res += "Left,"
        if key & FROM_LEFT_2ND_BUTTON_PRESSED:
            res += "2,"
        if key & FROM_LEFT_3RD_BUTTON_PRESSED:
            res += "3,"
        if key & FROM_LEFT_4TH_BUTTON_PRESSED:
            res += "4,"
        if key & RIGHTMOST_BUTTON_PRESSED:
            res += "Right,"
        if len(res) > 0:
            res = res[:-1]
        return res

    def mouse_types(flag: int):
        if flag == 0:
            return "press/release"
        if flag == DOUBLE_CLICK:
            return "double click"
        if flag == MOUSE_HWHEELED:
            return "wheel horizontal"
        if flag == MOUSE_MOVED:
            return "move"
        if flag == MOUSE_WHEELED:
            return "wheel vertical"

    class CHAR_UNION(Union):
        _fields_ = [("UnicodeChar", c_wchar), ("AsciiChar", c_char)]

        def __str__(self) -> str:
            return repr(self.UnicodeChar)

    class KEY_EVENT_RECORD(Structure):
        _fields_ = [
            ("bKeyDown", c_byte),
            ("pad2", c_byte),
            ("pad1", c_short),
            ("wRepeatCount", c_short),
            ("wVirtualKeyCode", c_short),
            ("wVirtualScanCode", c_short),
            ("uChar", CHAR_UNION),
            ("dwControlKeyState", c_int),
        ]

        def __str__(self) -> str:
            return f"{self.uChar} [isDown={'True' if self.bKeyDown else 'False'}, repeatCount={self.wRepeatCount}, modifiers=[{modifiers(self.dwControlKeyState)}]]"

    class COORD(Structure):
        _fields_ = [("X", SHORT), ("Y", SHORT)]

        def __str__(self) -> str:
            return f"{self.X},{self.Y}"

    class MOUSE_EVENT_RECORD(Structure):
        _fields_ = [
            ("dwMousePosition", COORD),
            ("dwButtonState", DWORD),
            ("dwControlKeyState", DWORD),
            ("dwEventFlags", DWORD),
        ]

        def __str__(self) -> str:
            return f"{self.dwMousePosition} [type={mouse_types(self.dwEventFlags)}, buttons={mouse_keys(self.dwButtonState)}, modifiers={modifiers(self.dwControlKeyState)}]"

    class WINDOW_BUFFER_SIZE_RECORD(Structure):
        _fields_ = [("dwSize", COORD)]

        def __str__(self) -> str:
            return str(self.dwSize)

    class MENU_EVENT_RECORD(Structure):
        _fields_ = [("dwCommandId", UINT)]

        def __str__(self) -> str:
            return ""

    class FOCUS_EVENT_RECORD(Structure):
        _fields_ = [("bSetFocus", BOOL)]

        def __str__(self) -> str:
            if self.bSetFocus:
                return "True"
            else:
                return "False"

    class Event(Union):
        _fields_ = [
            ("KeyEvent", KEY_EVENT_RECORD),
            ("MouseEvent", MOUSE_EVENT_RECORD),
            ("WindowBufferSizeEvent", WINDOW_BUFFER_SIZE_RECORD),
            ("MenuEvent", MENU_EVENT_RECORD),
            ("FocusEvent", FOCUS_EVENT_RECORD),
        ]

    class INPUT_RECORD(Structure):
        _fields_ = [("EventType", WORD), ("Event", Event)]

        def __str__(self) -> str:
            if self.EventType == FOCUS_EVENT:
                event = str(self.Event.FocusEvent)
            elif self.EventType == KEY_EVENT:
                event = str(self.Event.KeyEvent)
            elif self.EventType == MENU_EVENT:
                event = str(self.Event.MenuEvent)
            elif self.EventType == MOUSE_EVENT:
                event = str(self.Event.MouseEvent)
            elif self.EventType == WINDOW_BUFFER_SIZE_EVENT:
                event = str(self.Event.WindowBufferSizeEvent)
            else:
                event = "Unknown event"

            return f"{translation_table[self.EventType]} [{event}]"

    FOCUS_EVENT = 0x0010
    KEY_EVENT = 0x0001
    MENU_EVENT = 0x0008
    MOUSE_EVENT = 0x0002
    WINDOW_BUFFER_SIZE_EVENT = 0x0004

    translation_table = {
        0x0010: "FOCUS_EVENT",
        0x0001: "KEY_EVENT",
        0x0008: "MENU_EVENT",
        0x0002: "MOUSE_EVENT",
        0x0004: "WINDOW_BUFFER_SIZE_EVENT",
    }
