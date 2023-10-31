import os

if os.name != "nt":
    import select
    import sys
    import termios
    import fcntl
    from .common import Key, Mouse, MouseType
    from .utils import split_lines_width, remove_control_chars, length

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
        global oldterm, oldflags
        execute_ansii_escape_sequence("[?1049h")
        execute_ansii_escape_sequence("[?1003h\n")
        fileno = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fileno)
        newattr = termios.tcgetattr(fileno)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fileno, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fileno, fcntl.F_GETFL)
        fcntl.fcntl(fileno, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        hide_cursor()
        clear_screen()

    def stop():
        show_cursor()
        fileno = sys.stdin.fileno()
        termios.tcsetattr(fileno, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fileno, fcntl.F_SETFL, oldflags)
        execute_ansii_escape_sequence("[?1003l\n")
        execute_ansii_escape_sequence("[?1049l")

    def is_focused() -> bool:
        assert False, "LINUX UNINPLEMENTED"

    def isData():
        return select.select([sys.stdin], [], [], 0)

    def poll_events() -> Key | Mouse | None:
        try:
            c = os.read(sys.stdin.fileno(), 8)
            if len(c) == 0:
                return None
            if c[0] != 0x1B:
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code=c.decode(),
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )

            if len(c) == 1:
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="^[",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )

            if c[1:3] == b"[M":
                if c[3] == 32:
                    return Mouse(
                        position=(0, 0),
                        type_=MouseType.PRESSED_CHANGE,
                        buttons=[1],
                        scroll=(0, 0),
                        capslock=False,
                        enhanced=False,
                        left_alt=False,
                        left_ctrl=False,
                        numlock=False,
                        right_alt=False,
                        right_ctrl=False,
                        scrolllock=False,
                        shift=False,
                    )
                if c[3] == 33:
                    return Mouse(
                        position=(0, 0),
                        type_=MouseType.PRESSED_CHANGE,
                        buttons=[1],
                        scroll=(0, 0),
                        capslock=False,
                        enhanced=False,
                        left_alt=False,
                        left_ctrl=False,
                        numlock=False,
                        right_alt=False,
                        right_ctrl=False,
                        scrolllock=False,
                        shift=False,
                    )
                if c[3] == 34:
                    return Mouse(
                        position=(0, 0),
                        type_=MouseType.PRESSED_CHANGE,
                        buttons=[2],
                        scroll=(0, 0),
                        capslock=False,
                        enhanced=False,
                        left_alt=False,
                        left_ctrl=False,
                        numlock=False,
                        right_alt=False,
                        right_ctrl=False,
                        scrolllock=False,
                        shift=False,
                    )
                if c[3] == 35:
                    return Mouse(
                        position=(0, 0),
                        type_=MouseType.PRESSED_CHANGE,
                        buttons=[],
                        scroll=(0, 0),
                        capslock=False,
                        enhanced=False,
                        left_alt=False,
                        left_ctrl=False,
                        numlock=False,
                        right_alt=False,
                        right_ctrl=False,
                        scrolllock=False,
                        shift=False,
                    )
                if c[3] in (64, 65, 66, 67):
                    return Mouse(
                        position=(0, 0),
                        type_=MouseType.MOVE,
                        buttons=[],
                        scroll=(0, 0),
                        capslock=False,
                        enhanced=False,
                        left_alt=False,
                        left_ctrl=False,
                        numlock=False,
                        right_alt=False,
                        right_ctrl=False,
                        scrolllock=False,
                        shift=False,
                    )
                if c[3] == 96:
                    return Mouse(
                        position=(0, 0),
                        type_=MouseType.SCROLL,
                        buttons=[],
                        scroll=(0, 1),
                        capslock=False,
                        enhanced=False,
                        left_alt=False,
                        left_ctrl=False,
                        numlock=False,
                        right_alt=False,
                        right_ctrl=False,
                        scrolllock=False,
                        shift=False,
                    )
                if c[3] == 97:
                    return Mouse(
                        position=(0, 0),
                        type_=MouseType.SCROLL,
                        buttons=[],
                        scroll=(0, -1),
                        capslock=False,
                        enhanced=False,
                        left_alt=False,
                        left_ctrl=False,
                        numlock=False,
                        right_alt=False,
                        right_ctrl=False,
                        scrolllock=False,
                        shift=False,
                    )
            if c == b"\x1b[A":
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_UP",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c == b"\x1b[B":
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_DOWN",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c == b"\x1b[C":
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_RIGHT",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c == b"\x1b[D":
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_LEFT",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1bOP",
                b"\x1b[11~",
                "\x1bOP",
                b"\x1b[11~",
                b"\x1bOP",
                b"\x1bOP",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(1)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1bOQ",
                b"\x1b[12~",
                b"\x1bOQ",
                b"\x1b[12~",
                b"\x1bOQ",
                b"\x1bOQ",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(2)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1bOR",
                b"\x1b[13~",
                b"\x1bOR",
                b"\x1b[13~",
                b"\x1bOR",
                b"\x1bOR",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(3)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1bOS",
                b"\x1b[14~",
                b"\x1bOS",
                b"\x1b[14~",
                b"\x1bOS",
                b"\x1bOS",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(4)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[15~", b"\x1b[15~", b"\x1b[15~", b"\x1b[15~", b"\x1b[15~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(5)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[17~",
                b"\x1b[17~",
                b"\x1b[17~",
                b"\x1b[17~",
                b"\x1b[17~",
                b"\x1b[17~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(6)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[18~",
                b"\x1b[18~",
                b"\x1b[18~",
                b"\x1b[18~",
                b"\x1b[18~",
                b"\x1b[18~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(7)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[19~",
                b"\x1b[19~",
                b"\x1b[19~",
                b"\x1b[19~",
                b"\x1b[19~",
                b"\x1b[19~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(8)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[20~",
                b"\x1b[20~",
                b"\x1b[20~",
                b"\x1b[20~",
                b"\x1b[20~",
                b"\x1b[20~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(9)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[21~",
                b"\x1b[21~",
                b"\x1b[21~",
                b"\x1b[21~",
                b"\x1b[21~",
                b"\x1b[21~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(10)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[23~",
                b"\x1b[23~",
                b"\x1b[23~",
                b"\x1b[23~",
                b"\x1b[23~",
                b"\x1b[23~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(11)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[24~",
                b"\x1b[24~",
                b"\x1b[24~",
                b"\x1b[24~",
                b"\x1b[24~",
                b"\x1b[24~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(12)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[25~", b"\x1b[11;2~", b"\x1bO2P", b"\x1b[25~", b"\x1b[25~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(13)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[26~", b"\x1b[12;2~", b"\x1bO2Q", b"\x1b[26~", b"\x1b[26~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(14)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[28~", b"\x1b[13;2~", b"\x1bO2R", b"\x1b[28~", b"\x1b[28~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(15)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[29~", b"\x1b[14;2~", b"\x1bO2S", b"\x1b[29~", b"\x1b[29~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(16)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[31~",
                b"\x1b[15;2~",
                b"\x1b[15;2~",
                b"\x1b[31~",
                b"\x1b[31~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(17)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[32~",
                b"\x1b[17;2~",
                b"\x1b[17;2~",
                b"\x1b[32~",
                b"\x1b[32~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(18)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[33~",
                b"\x1b[18;2~",
                b"\x1b[18;2~",
                b"\x1b[33~",
                b"\x1b[33~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(19)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (
                b"\x1b[34~",
                b"\x1b[19;2~",
                b"\x1b[19;2~",
                b"\x1b[34~",
                b"\x1b[34~",
            ):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(20)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[20;2~", b"\x1b[20;2~", b"\x1b[23$"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(21)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[21;2~", b"\x1b[21;2~", b"\x1b[24$"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(22)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[23;2~", b"\x1b[23;2~", b"\x1b[11^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(23)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[24;2~", b"\x1b[24;2~", b"\x1b[12^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(24)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[11;5~", b"\x1bO5P", b"\x1b[13^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(25)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[12;5~", b"\x1bO5Q", b"\x1b[14^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(26)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[13;5~", b"\x1bO5R", b"\x1b[15^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(27)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[14;5~", b"\x1bO5S", b"\x1b[17^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(28)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[15;5~", b"\x1b[15;5~", b"\x1b[18^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(29)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[17;5~", b"\x1b[17;5~", b"\x1b[19^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(30)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[18;5~", b"\x1b[18;5~", b"\x1b[20^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(31)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[19;5~", b"\x1b[19;5~", b"\x1b[21^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(32)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[20;5~", b"\x1b[20;5~", b"\x1b[23^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(33)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[21;5~", b"\x1b[21;5~", b"\x1b[24^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(34)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[23;5~", b"\x1b[23;5~", b"\x1b[25^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(35)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[24;5~", b"\x1b[24;5~", b"\x1b[26^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(36)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[11;6~", b"\x1bO6P", b"\x1b[28^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(37)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[12;6~", b"\x1bO6Q", b"\x1b[29^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(38)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[13;6~", b"\x1bO6R", b"\x1b[31^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(39)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[14;6~", b"\x1bO6S", b"\x1b[32^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(40)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[15;6~", b"\x1b[15;6~", b"\x1b[33^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(41)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[17;6~", b"\x1b[17;6~", b"\x1b[34^"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(42)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[18;6~", b"\x1b[18;6~", b"\x1b[23@"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(43)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[19;6~", b"\x1b[19;6~", b"\x1b[24@"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(44)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[20;6~", b"\x1b[20; 6~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(45)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[21;6~", b"\x1b[21; 6~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(46)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[23;6~", b"\x1b[23; 6~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(47)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )
            if c in (b"\x1b[24;6~", b"\x1b[24; 6~"):
                return Key(
                    pressed=True,
                    char=c.decode(),
                    code="KEY_F(48)",
                    repeat_count=1,
                    capslock=False,
                    enhanced=False,
                    left_alt=False,
                    left_ctrl=False,
                    numlock=False,
                    right_alt=False,
                    right_ctrl=False,
                    scrolllock=False,
                    shift=False,
                )

            return Key(
                pressed=False,
                char=c.decode(),
                code="UNKOWN",
                repeat_count=0,
                capslock=False,
                enhanced=False,
                left_alt=False,
                left_ctrl=False,
                numlock=False,
                right_alt=False,
                right_ctrl=False,
                scrolllock=False,
                shift=False,
            )
        except IOError:
            return None

    def get_size() -> tuple[int, int]:
        size = os.get_terminal_size()
        return size.lines, size.columns

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
