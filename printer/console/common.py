from enum import Enum


def modifiers(
    capslock: bool,
    enhanced: bool,
    left_alt: bool,
    left_ctrl: bool,
    numlock: bool,
    right_alt: bool,
    right_ctrl: bool,
    scrolllock: bool,
    shift: bool,
) -> str:
    res = ""
    if capslock:
        res += "CapsLock,"
    if enhanced:
        res += "Enhance,"
    if left_alt:
        res += "LeftAlt,"
    if left_ctrl:
        res += "LeftCtrl,"
    if numlock:
        res += "NumLock,"
    if right_alt:
        res += "RighttAlt,"
    if right_ctrl:
        res += "RightCtrl,"
    if scrolllock:
        res += "ScrollLock,"
    if shift:
        res += "Shift,"

    if len(res) > 0:
        res = res[:-1]
    return res


class Key:
    def __init__(
        self,
        *,
        pressed: bool,
        char: str,
        code: str,
        repeat_count: int,
        capslock: bool,
        enhanced: bool,
        left_alt: bool,
        left_ctrl: bool,
        numlock: bool,
        right_alt: bool,
        right_ctrl: bool,
        scrolllock: bool,
        shift: bool,
    ) -> None:
        self.pressed = pressed
        self.value = char
        self.code = code
        self.repeat_count = repeat_count
        self.capslock = capslock
        self.enhanced = enhanced
        self.left_alt = left_alt
        self.left_ctrl = left_ctrl
        self.numlock = numlock
        self.right_alt = right_alt
        self.right_ctrl = right_ctrl
        self.scrolllock = scrolllock
        self.shift = shift

    def __str__(self) -> str:
        return f"Key {repr(self.value)} {{{repr(self.code)}}} [pressed = {self.pressed}, repeat = {self.repeat_count}, modifiers = [{modifiers(self.capslock ,self.enhanced ,self.left_alt ,self.left_ctrl ,self.numlock ,self.right_alt ,self.right_ctrl ,self.scrolllock ,self.shift)}]]"


class MouseType(Enum):
    MOVE = 0
    PRESSED_CHANGE = 1
    DOUBLE_CLICK = 2
    SCROLL = 3


class Mouse:
    def __init__(
        self,
        *,
        position: tuple[int, int],
        type_: MouseType,
        buttons: list[int],
        scroll: tuple[float, float],
        capslock: bool,
        enhanced: bool,
        left_alt: bool,
        left_ctrl: bool,
        numlock: bool,
        right_alt: bool,
        right_ctrl: bool,
        scrolllock: bool,
        shift: bool,
    ) -> None:
        self.position = position
        self.type_ = type_
        self.buttons = buttons
        self.scroll = scroll
        self.capslock = capslock
        self.enhanced = enhanced
        self.left_alt = left_alt
        self.left_ctrl = left_ctrl
        self.numlock = numlock
        self.right_alt = right_alt
        self.right_ctrl = right_ctrl
        self.scrolllock = scrolllock
        self.shift = shift

    def __str__(self) -> str:
        return f"Mouse {self.position},{self.scroll} [buttons = {self.buttons}, type = {self.type_}, modifiers = [{modifiers(self.capslock ,self.enhanced ,self.left_alt ,self.left_ctrl ,self.numlock ,self.right_alt ,self.right_ctrl ,self.scrolllock ,self.shift)}]]"
