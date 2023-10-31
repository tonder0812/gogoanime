"""
Taken from PDCurses (https://github.com/wmcbrine/PDCurses) and then adapted
"""
import os

if os.name == "nt":
    from .windows_events import (
        ENHANCED_KEY,
        KEY_EVENT_RECORD,
        LEFT_ALT_PRESSED,
        LEFT_CTRL_PRESSED,
        RIGHT_ALT_PRESSED,
        RIGHT_CTRL_PRESSED,
        SHIFT_PRESSED,
    )
    from .windows_api import user32

    VK_SHIFT = 0x10
    VK_CONTROL = 0x11
    VK_MENU = 0x12
    VK_PAUSE = 0x13
    VK_CAPITAL = 0x14
    VK_NUMLOCK = 0x90
    VK_SCROLL = 0x91
    VK_LSHIFT = 0xA0
    VK_RSHIFT = 0xA1
    VK_LCONTROL = 0xA2
    VK_RCONTROL = 0xA3
    VK_LMENU = 0xA4
    VK_RMENU = 0xA5

    KEY_CODE_YES = 0x100

    KEY_BREAK = 0x101
    KEY_DOWN = 0x102
    KEY_UP = 0x103
    KEY_LEFT = 0x104
    KEY_RIGHT = 0x105
    KEY_HOME = 0x106
    KEY_BACKSPACE = 0x107
    KEY_F0 = 0x108

    KEY_DL = 0x148
    KEY_IL = 0x149
    KEY_DC = 0x14A
    KEY_IC = 0x14B
    KEY_EIC = 0x14C
    KEY_CLEAR = 0x14D
    KEY_EOS = 0x14E
    KEY_EOL = 0x14F
    KEY_SF = 0x150
    KEY_SR = 0x151
    KEY_NPAGE = 0x152
    KEY_PPAGE = 0x153
    KEY_STAB = 0x154
    KEY_CTAB = 0x155
    KEY_CATAB = 0x156
    KEY_ENTER = 0x157
    KEY_SRESET = 0x158
    KEY_RESET = 0x159
    KEY_PRINT = 0x15A
    KEY_LL = 0x15B
    KEY_ABORT = 0x15C
    KEY_SHELP = 0x15D
    KEY_LHELP = 0x15E
    KEY_BTAB = 0x15F
    KEY_BEG = 0x160
    KEY_CANCEL = 0x161
    KEY_CLOSE = 0x162
    KEY_COMMAND = 0x163
    KEY_COPY = 0x164
    KEY_CREATE = 0x165
    KEY_END = 0x166
    KEY_EXIT = 0x167
    KEY_FIND = 0x168
    KEY_HELP = 0x169
    KEY_MARK = 0x16A
    KEY_MESSAGE = 0x16B
    KEY_MOVE = 0x16C
    KEY_NEXT = 0x16D
    KEY_OPEN = 0x16E
    KEY_OPTIONS = 0x16F
    KEY_PREVIOUS = 0x170
    KEY_REDO = 0x171
    KEY_REFERENCE = 0x172
    KEY_REFRESH = 0x173
    KEY_REPLACE = 0x174
    KEY_RESTART = 0x175
    KEY_RESUME = 0x176
    KEY_SAVE = 0x177
    KEY_SBEG = 0x178
    KEY_SCANCEL = 0x179
    KEY_SCOMMAND = 0x17A
    KEY_SCOPY = 0x17B
    KEY_SCREATE = 0x17C
    KEY_SDC = 0x17D
    KEY_SDL = 0x17E
    KEY_SELECT = 0x17F
    KEY_SEND = 0x180
    KEY_SEOL = 0x181
    KEY_SEXIT = 0x182
    KEY_SFIND = 0x183
    KEY_SHOME = 0x184
    KEY_SIC = 0x185

    KEY_SLEFT = 0x187
    KEY_SMESSAGE = 0x188
    KEY_SMOVE = 0x189
    KEY_SNEXT = 0x18A
    KEY_SOPTIONS = 0x18B
    KEY_SPREVIOUS = 0x18C
    KEY_SPRINT = 0x18D
    KEY_SREDO = 0x18E
    KEY_SREPLACE = 0x18F
    KEY_SRIGHT = 0x190
    KEY_SRSUME = 0x191
    KEY_SSAVE = 0x192
    KEY_SSUSPEND = 0x193
    KEY_SUNDO = 0x194
    KEY_SUSPEND = 0x195
    KEY_UNDO = 0x196

    ALT_0 = 0x197
    ALT_1 = 0x198
    ALT_2 = 0x199
    ALT_3 = 0x19A
    ALT_4 = 0x19B
    ALT_5 = 0x19C
    ALT_6 = 0x19D
    ALT_7 = 0x19E
    ALT_8 = 0x19F
    ALT_9 = 0x1A0
    ALT_A = 0x1A1
    ALT_B = 0x1A2
    ALT_C = 0x1A3
    ALT_D = 0x1A4
    ALT_E = 0x1A5
    ALT_F = 0x1A6
    ALT_G = 0x1A7
    ALT_H = 0x1A8
    ALT_I = 0x1A9
    ALT_J = 0x1AA
    ALT_K = 0x1AB
    ALT_L = 0x1AC
    ALT_M = 0x1AD
    ALT_N = 0x1AE
    ALT_O = 0x1AF
    ALT_P = 0x1B0
    ALT_Q = 0x1B1
    ALT_R = 0x1B2
    ALT_S = 0x1B3
    ALT_T = 0x1B4
    ALT_U = 0x1B5
    ALT_V = 0x1B6
    ALT_W = 0x1B7
    ALT_X = 0x1B8
    ALT_Y = 0x1B9
    ALT_Z = 0x1BA

    CTL_LEFT = 0x1BB
    CTL_RIGHT = 0x1BC
    CTL_PGUP = 0x1BD
    CTL_PGDN = 0x1BE
    CTL_HOME = 0x1BF
    CTL_END = 0x1C0

    KEY_A1 = 0x1C1
    KEY_A2 = 0x1C2
    KEY_A3 = 0x1C3
    KEY_B1 = 0x1C4
    KEY_B2 = 0x1C5
    KEY_B3 = 0x1C6
    KEY_C1 = 0x1C7
    KEY_C2 = 0x1C8
    KEY_C3 = 0x1C9

    PADSLASH = 0x1CA
    PADENTER = 0x1CB
    CTL_PADENTER = 0x1CC
    ALT_PADENTER = 0x1CD
    PADSTOP = 0x1CE
    PADSTAR = 0x1CF
    PADMINUS = 0x1D0
    PADPLUS = 0x1D1
    CTL_PADSTOP = 0x1D2
    CTL_PADCENTER = 0x1D3
    CTL_PADPLUS = 0x1D4
    CTL_PADMINUS = 0x1D5
    CTL_PADSLASH = 0x1D6
    CTL_PADSTAR = 0x1D7
    ALT_PADPLUS = 0x1D8
    ALT_PADMINUS = 0x1D9
    ALT_PADSLASH = 0x1DA
    ALT_PADSTAR = 0x1DB
    ALT_PADSTOP = 0x1DC
    CTL_INS = 0x1DD
    ALT_DEL = 0x1DE
    ALT_INS = 0x1DF
    CTL_UP = 0x1E0
    CTL_DOWN = 0x1E1
    CTL_TAB = 0x1E2
    ALT_TAB = 0x1E3
    ALT_MINUS = 0x1E4
    ALT_EQUAL = 0x1E5
    ALT_HOME = 0x1E6
    ALT_PGUP = 0x1E7
    ALT_PGDN = 0x1E8
    ALT_END = 0x1E9
    ALT_UP = 0x1EA
    ALT_DOWN = 0x1EB
    ALT_RIGHT = 0x1EC
    ALT_LEFT = 0x1ED
    ALT_ENTER = 0x1EE
    ALT_ESC = 0x1EF
    ALT_BQUOTE = 0x1F0
    ALT_LBRACKET = 0x1F1
    ALT_RBRACKET = 0x1F2
    ALT_SEMICOLON = 0x1F3
    ALT_FQUOTE = 0x1F4
    ALT_COMMA = 0x1F5
    ALT_STOP = 0x1F6
    ALT_FSLASH = 0x1F7
    ALT_BKSP = 0x1F8
    CTL_BKSP = 0x1F9
    PAD0 = 0x1FA

    CTL_PAD0 = 0x1FB
    CTL_PAD1 = 0x1FC
    CTL_PAD2 = 0x1FD
    CTL_PAD3 = 0x1FE
    CTL_PAD4 = 0x1FF
    CTL_PAD5 = 0x200
    CTL_PAD6 = 0x201
    CTL_PAD7 = 0x202
    CTL_PAD8 = 0x203
    CTL_PAD9 = 0x204

    ALT_PAD0 = 0x205
    ALT_PAD1 = 0x206
    ALT_PAD2 = 0x207
    ALT_PAD3 = 0x208
    ALT_PAD4 = 0x209
    ALT_PAD5 = 0x20A
    ALT_PAD6 = 0x20B
    ALT_PAD7 = 0x20C
    ALT_PAD8 = 0x20D
    ALT_PAD9 = 0x20E

    CTL_DEL = 0x20F
    ALT_BSLASH = 0x210
    CTL_ENTER = 0x211

    SHF_PADENTER = 0x212
    SHF_PADSLASH = 0x213
    SHF_PADSTAR = 0x214
    SHF_PADPLUS = 0x215
    SHF_PADMINUS = 0x216
    SHF_UP = 0x217
    SHF_DOWN = 0x218
    SHF_IC = 0x219
    SHF_DC = 0x21A

    KEY_MOUSE = 0x21B
    KEY_SHIFT_L = 0x21C
    KEY_SHIFT_R = 0x21D
    KEY_CONTROL_L = 0x21E
    KEY_CONTROL_R = 0x21F
    KEY_ALT_L = 0x220
    KEY_ALT_R = 0x221
    KEY_RESIZE = 0x222
    KEY_SUP = 0x223
    KEY_SDOWN = 0x224

    KEY_MIN = KEY_BREAK
    KEY_MAX = KEY_SDOWN

    names = [
        "KEY_BREAK",
        "KEY_DOWN",
        "KEY_UP",
        "KEY_LEFT",
        "KEY_RIGHT",
        "KEY_HOME",
        "KEY_BACKSPACE",
        "KEY_F0",
        "KEY_F(1)",
        "KEY_F(2)",
        "KEY_F(3)",
        "KEY_F(4)",
        "KEY_F(5)",
        "KEY_F(6)",
        "KEY_F(7)",
        "KEY_F(8)",
        "KEY_F(9)",
        "KEY_F(10)",
        "KEY_F(11)",
        "KEY_F(12)",
        "KEY_F(13)",
        "KEY_F(14)",
        "KEY_F(15)",
        "KEY_F(16)",
        "KEY_F(17)",
        "KEY_F(18)",
        "KEY_F(19)",
        "KEY_F(20)",
        "KEY_F(21)",
        "KEY_F(22)",
        "KEY_F(23)",
        "KEY_F(24)",
        "KEY_F(25)",
        "KEY_F(26)",
        "KEY_F(27)",
        "KEY_F(28)",
        "KEY_F(29)",
        "KEY_F(30)",
        "KEY_F(31)",
        "KEY_F(32)",
        "KEY_F(33)",
        "KEY_F(34)",
        "KEY_F(35)",
        "KEY_F(36)",
        "KEY_F(37)",
        "KEY_F(38)",
        "KEY_F(39)",
        "KEY_F(40)",
        "KEY_F(41)",
        "KEY_F(42)",
        "KEY_F(43)",
        "KEY_F(44)",
        "KEY_F(45)",
        "KEY_F(46)",
        "KEY_F(47)",
        "KEY_F(48)",
        "KEY_F(49)",
        "KEY_F(50)",
        "KEY_F(51)",
        "KEY_F(52)",
        "KEY_F(53)",
        "KEY_F(54)",
        "KEY_F(55)",
        "KEY_F(56)",
        "KEY_F(57)",
        "KEY_F(58)",
        "KEY_F(59)",
        "KEY_F(60)",
        "KEY_F(61)",
        "KEY_F(62)",
        "KEY_F(63)",
        "KEY_DL",
        "KEY_IL",
        "KEY_DC",
        "KEY_IC",
        "KEY_EIC",
        "KEY_CLEAR",
        "KEY_EOS",
        "KEY_EOL",
        "KEY_SF",
        "KEY_SR",
        "KEY_NPAGE",
        "KEY_PPAGE",
        "KEY_STAB",
        "KEY_CTAB",
        "KEY_CATAB",
        "KEY_ENTER",
        "KEY_SRESET",
        "KEY_RESET",
        "KEY_PRINT",
        "KEY_LL",
        "KEY_ABORT",
        "KEY_SHELP",
        "KEY_LHELP",
        "KEY_BTAB",
        "KEY_BEG",
        "KEY_CANCEL",
        "KEY_CLOSE",
        "KEY_COMMAND",
        "KEY_COPY",
        "KEY_CREATE",
        "KEY_END",
        "KEY_EXIT",
        "KEY_FIND",
        "KEY_HELP",
        "KEY_MARK",
        "KEY_MESSAGE",
        "KEY_MOVE",
        "KEY_NEXT",
        "KEY_OPEN",
        "KEY_OPTIONS",
        "KEY_PREVIOUS",
        "KEY_REDO",
        "KEY_REFERENCE",
        "KEY_REFRESH",
        "KEY_REPLACE",
        "KEY_RESTART",
        "KEY_RESUME",
        "KEY_SAVE",
        "KEY_SBEG",
        "KEY_SCANCEL",
        "KEY_SCOMMAND",
        "KEY_SCOPY",
        "KEY_SCREATE",
        "KEY_SDC",
        "KEY_SDL",
        "KEY_SELECT",
        "KEY_SEND",
        "KEY_SEOL",
        "KEY_SEXIT",
        "KEY_SFIND",
        "KEY_SHOME",
        "KEY_SIC",
        "UNKNOWN KEY",
        "KEY_SLEFT",
        "KEY_SMESSAGE",
        "KEY_SMOVE",
        "KEY_SNEXT",
        "KEY_SOPTIONS",
        "KEY_SPREVIOUS",
        "KEY_SPRINT",
        "KEY_SREDO",
        "KEY_SREPLACE",
        "KEY_SRIGHT",
        "KEY_SRSUME",
        "KEY_SSAVE",
        "KEY_SSUSPEND",
        "KEY_SUNDO",
        "KEY_SUSPEND",
        "KEY_UNDO",
        "ALT_0",
        "ALT_1",
        "ALT_2",
        "ALT_3",
        "ALT_4",
        "ALT_5",
        "ALT_6",
        "ALT_7",
        "ALT_8",
        "ALT_9",
        "ALT_A",
        "ALT_B",
        "ALT_C",
        "ALT_D",
        "ALT_E",
        "ALT_F",
        "ALT_G",
        "ALT_H",
        "ALT_I",
        "ALT_J",
        "ALT_K",
        "ALT_L",
        "ALT_M",
        "ALT_N",
        "ALT_O",
        "ALT_P",
        "ALT_Q",
        "ALT_R",
        "ALT_S",
        "ALT_T",
        "ALT_U",
        "ALT_V",
        "ALT_W",
        "ALT_X",
        "ALT_Y",
        "ALT_Z",
        "CTL_LEFT",
        "CTL_RIGHT",
        "CTL_PGUP",
        "CTL_PGDN",
        "CTL_HOME",
        "CTL_END",
        "KEY_A1",
        "KEY_A2",
        "KEY_A3",
        "KEY_B1",
        "KEY_B2",
        "KEY_B3",
        "KEY_C1",
        "KEY_C2",
        "KEY_C3",
        "PADSLASH",
        "PADENTER",
        "CTL_PADENTER",
        "ALT_PADENTER",
        "PADSTOP",
        "PADSTAR",
        "PADMINUS",
        "PADPLUS",
        "CTL_PADSTOP",
        "CTL_PADCENTER",
        "CTL_PADPLUS",
        "CTL_PADMINUS",
        "CTL_PADSLASH",
        "CTL_PADSTAR",
        "ALT_PADPLUS",
        "ALT_PADMINUS",
        "ALT_PADSLASH",
        "ALT_PADSTAR",
        "ALT_PADSTOP",
        "CTL_INS",
        "ALT_DEL",
        "ALT_INS",
        "CTL_UP",
        "CTL_DOWN",
        "CTL_TAB",
        "ALT_TAB",
        "ALT_MINUS",
        "ALT_EQUAL",
        "ALT_HOME",
        "ALT_PGUP",
        "ALT_PGDN",
        "ALT_END",
        "ALT_UP",
        "ALT_DOWN",
        "ALT_RIGHT",
        "ALT_LEFT",
        "ALT_ENTER",
        "ALT_ESC",
        "ALT_BQUOTE",
        "ALT_LBRACKET",
        "ALT_RBRACKET",
        "ALT_SEMICOLON",
        "ALT_FQUOTE",
        "ALT_COMMA",
        "ALT_STOP",
        "ALT_FSLASH",
        "ALT_BKSP",
        "CTL_BKSP",
        "PAD0",
        "CTL_PAD0",
        "CTL_PAD1",
        "CTL_PAD2",
        "CTL_PAD3",
        "CTL_PAD4",
        "CTL_PAD5",
        "CTL_PAD6",
        "CTL_PAD7",
        "CTL_PAD8",
        "CTL_PAD9",
        "ALT_PAD0",
        "ALT_PAD1",
        "ALT_PAD2",
        "ALT_PAD3",
        "ALT_PAD4",
        "ALT_PAD5",
        "ALT_PAD6",
        "ALT_PAD7",
        "ALT_PAD8",
        "ALT_PAD9",
        "CTL_DEL",
        "ALT_BSLASH",
        "CTL_ENTER",
        "SHF_PADENTER",
        "SHF_PADSLASH",
        "SHF_PADSTAR",
        "SHF_PADPLUS",
        "SHF_PADMINUS",
        "SHF_UP",
        "SHF_DOWN",
        "SHF_IC",
        "SHF_DC",
        "KEY_MOUSE",
        "KEY_SHIFT_L",
        "KEY_SHIFT_R",
        "KEY_CONTROL_L",
        "KEY_CONTROL_R",
        "KEY_ALT_L",
        "KEY_ALT_R",
        "KEY_RESIZE",
        "KEY_SUP",
        "KEY_SDOWN",
    ]
    A_CHARTEXT = 0x0000FFFF

    def has_key(key: int) -> bool:
        return key >= KEY_MIN and key <= KEY_MAX

    def unctrl(c: int) -> str:
        ic = c & A_CHARTEXT

        if ic >= 0x20 and ic != 0x7F:
            return chr(ic)

        if ic == 0x7F:
            return "^?"

        return "^" + chr(ic + ord("@"))

    def get_name(key: int) -> str:
        if key == ord("\r"):
            return "\n"
        return (
            unctrl(key)
            if ((key >= 0) and (key < 0x80))
            else (names[key - KEY_MIN] if has_key(key) else "UNKNOWN KEY")
        )

    def KEY_F(n: int) -> int:
        return KEY_F0 + n

    kptab: list[dict[str, int]] = [
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {
            "normal": 0x08,
            "shift": 0x08,
            "control": 0x7F,
            "alt": ALT_BKSP,
            "extended": 0,
        },
        {
            "normal": 0x09,
            "shift": KEY_BTAB,
            "control": CTL_TAB,
            "alt": ALT_TAB,
            "extended": 999,
        },
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {
            "normal": KEY_B2,
            "shift": 0x35,
            "control": CTL_PAD5,
            "alt": ALT_PAD5,
            "extended": 0,
        },
        {
            "normal": 0x0D,
            "shift": 0x0D,
            "control": CTL_ENTER,
            "alt": ALT_ENTER,
            "extended": 1,
        },
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0x1B, "shift": 0x1B, "control": 0x1B, "alt": ALT_ESC, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0x20, "shift": 0x20, "control": 0x20, "alt": 0x20, "extended": 0},
        {
            "normal": KEY_A3,
            "shift": 0x39,
            "control": CTL_PAD9,
            "alt": ALT_PAD9,
            "extended": 3,
        },
        {
            "normal": KEY_C3,
            "shift": 0x33,
            "control": CTL_PAD3,
            "alt": ALT_PAD3,
            "extended": 4,
        },
        {
            "normal": KEY_C1,
            "shift": 0x31,
            "control": CTL_PAD1,
            "alt": ALT_PAD1,
            "extended": 5,
        },
        {
            "normal": KEY_A1,
            "shift": 0x37,
            "control": CTL_PAD7,
            "alt": ALT_PAD7,
            "extended": 6,
        },
        {
            "normal": KEY_B1,
            "shift": 0x34,
            "control": CTL_PAD4,
            "alt": ALT_PAD4,
            "extended": 7,
        },
        {
            "normal": KEY_A2,
            "shift": 0x38,
            "control": CTL_PAD8,
            "alt": ALT_PAD8,
            "extended": 8,
        },
        {
            "normal": KEY_B3,
            "shift": 0x36,
            "control": CTL_PAD6,
            "alt": ALT_PAD6,
            "extended": 9,
        },
        {
            "normal": KEY_C2,
            "shift": 0x32,
            "control": CTL_PAD2,
            "alt": ALT_PAD2,
            "extended": 10,
        },
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {
            "normal": PAD0,
            "shift": 0x30,
            "control": CTL_PAD0,
            "alt": ALT_PAD0,
            "extended": 11,
        },
        {
            "normal": PADSTOP,
            "shift": 0x2E,
            "control": CTL_PADSTOP,
            "alt": ALT_PADSTOP,
            "extended": 12,
        },
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0x30, "shift": 0x29, "control": 0, "alt": ALT_0, "extended": 0},
        {"normal": 0x31, "shift": 0x21, "control": 0, "alt": ALT_1, "extended": 0},
        {"normal": 0x32, "shift": 0x40, "control": 0, "alt": ALT_2, "extended": 0},
        {"normal": 0x33, "shift": 0x23, "control": 0, "alt": ALT_3, "extended": 0},
        {"normal": 0x34, "shift": 0x24, "control": 0, "alt": ALT_4, "extended": 0},
        {"normal": 0x35, "shift": 0x25, "control": 0, "alt": ALT_5, "extended": 0},
        {"normal": 0x36, "shift": 0x5E, "control": 0, "alt": ALT_6, "extended": 0},
        {"normal": 0x37, "shift": 0x26, "control": 0, "alt": ALT_7, "extended": 0},
        {"normal": 0x38, "shift": 0x2A, "control": 0, "alt": ALT_8, "extended": 0},
        {"normal": 0x39, "shift": 0x28, "control": 0, "alt": ALT_9, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0x61, "shift": 0x41, "control": 0x01, "alt": ALT_A, "extended": 0},
        {"normal": 0x62, "shift": 0x42, "control": 0x02, "alt": ALT_B, "extended": 0},
        {"normal": 0x63, "shift": 0x43, "control": 0x03, "alt": ALT_C, "extended": 0},
        {"normal": 0x64, "shift": 0x44, "control": 0x04, "alt": ALT_D, "extended": 0},
        {"normal": 0x65, "shift": 0x45, "control": 0x05, "alt": ALT_E, "extended": 0},
        {"normal": 0x66, "shift": 0x46, "control": 0x06, "alt": ALT_F, "extended": 0},
        {"normal": 0x67, "shift": 0x47, "control": 0x07, "alt": ALT_G, "extended": 0},
        {"normal": 0x68, "shift": 0x48, "control": 0x08, "alt": ALT_H, "extended": 0},
        {"normal": 0x69, "shift": 0x49, "control": 0x09, "alt": ALT_I, "extended": 0},
        {"normal": 0x6A, "shift": 0x4A, "control": 0x0A, "alt": ALT_J, "extended": 0},
        {"normal": 0x6B, "shift": 0x4B, "control": 0x0B, "alt": ALT_K, "extended": 0},
        {"normal": 0x6C, "shift": 0x4C, "control": 0x0C, "alt": ALT_L, "extended": 0},
        {"normal": 0x6D, "shift": 0x4D, "control": 0x0D, "alt": ALT_M, "extended": 0},
        {"normal": 0x6E, "shift": 0x4E, "control": 0x0E, "alt": ALT_N, "extended": 0},
        {"normal": 0x6F, "shift": 0x4F, "control": 0x0F, "alt": ALT_O, "extended": 0},
        {"normal": 0x70, "shift": 0x50, "control": 0x10, "alt": ALT_P, "extended": 0},
        {"normal": 0x71, "shift": 0x51, "control": 0x11, "alt": ALT_Q, "extended": 0},
        {"normal": 0x72, "shift": 0x52, "control": 0x12, "alt": ALT_R, "extended": 0},
        {"normal": 0x73, "shift": 0x53, "control": 0x13, "alt": ALT_S, "extended": 0},
        {"normal": 0x74, "shift": 0x54, "control": 0x14, "alt": ALT_T, "extended": 0},
        {"normal": 0x75, "shift": 0x55, "control": 0x15, "alt": ALT_U, "extended": 0},
        {"normal": 0x76, "shift": 0x56, "control": 0x16, "alt": ALT_V, "extended": 0},
        {"normal": 0x77, "shift": 0x57, "control": 0x17, "alt": ALT_W, "extended": 0},
        {"normal": 0x78, "shift": 0x58, "control": 0x18, "alt": ALT_X, "extended": 0},
        {"normal": 0x79, "shift": 0x59, "control": 0x19, "alt": ALT_Y, "extended": 0},
        {"normal": 0x7A, "shift": 0x5A, "control": 0x1A, "alt": ALT_Z, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {
            "normal": 0x30,
            "shift": 0,
            "control": CTL_PAD0,
            "alt": ALT_PAD0,
            "extended": 0,
        },
        {
            "normal": 0x31,
            "shift": 0,
            "control": CTL_PAD1,
            "alt": ALT_PAD1,
            "extended": 0,
        },
        {
            "normal": 0x32,
            "shift": 0,
            "control": CTL_PAD2,
            "alt": ALT_PAD2,
            "extended": 0,
        },
        {
            "normal": 0x33,
            "shift": 0,
            "control": CTL_PAD3,
            "alt": ALT_PAD3,
            "extended": 0,
        },
        {
            "normal": 0x34,
            "shift": 0,
            "control": CTL_PAD4,
            "alt": ALT_PAD4,
            "extended": 0,
        },
        {
            "normal": 0x35,
            "shift": 0,
            "control": CTL_PAD5,
            "alt": ALT_PAD5,
            "extended": 0,
        },
        {
            "normal": 0x36,
            "shift": 0,
            "control": CTL_PAD6,
            "alt": ALT_PAD6,
            "extended": 0,
        },
        {
            "normal": 0x37,
            "shift": 0,
            "control": CTL_PAD7,
            "alt": ALT_PAD7,
            "extended": 0,
        },
        {
            "normal": 0x38,
            "shift": 0,
            "control": CTL_PAD8,
            "alt": ALT_PAD8,
            "extended": 0,
        },
        {
            "normal": 0x39,
            "shift": 0,
            "control": CTL_PAD9,
            "alt": ALT_PAD9,
            "extended": 0,
        },
        {
            "normal": PADSTAR,
            "shift": SHF_PADSTAR,
            "control": CTL_PADSTAR,
            "alt": ALT_PADSTAR,
            "extended": 999,
        },
        {
            "normal": PADPLUS,
            "shift": SHF_PADPLUS,
            "control": CTL_PADPLUS,
            "alt": ALT_PADPLUS,
            "extended": 999,
        },
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {
            "normal": PADMINUS,
            "shift": SHF_PADMINUS,
            "control": CTL_PADMINUS,
            "alt": ALT_PADMINUS,
            "extended": 999,
        },
        {
            "normal": 0x2E,
            "shift": 0,
            "control": CTL_PADSTOP,
            "alt": ALT_PADSTOP,
            "extended": 0,
        },
        {
            "normal": PADSLASH,
            "shift": SHF_PADSLASH,
            "control": CTL_PADSLASH,
            "alt": ALT_PADSLASH,
            "extended": 2,
        },
        {
            "normal": KEY_F(1),
            "shift": KEY_F(13),
            "control": KEY_F(25),
            "alt": KEY_F(37),
            "extended": 0,
        },
        {
            "normal": KEY_F(2),
            "shift": KEY_F(14),
            "control": KEY_F(26),
            "alt": KEY_F(38),
            "extended": 0,
        },
        {
            "normal": KEY_F(3),
            "shift": KEY_F(15),
            "control": KEY_F(27),
            "alt": KEY_F(39),
            "extended": 0,
        },
        {
            "normal": KEY_F(4),
            "shift": KEY_F(16),
            "control": KEY_F(28),
            "alt": KEY_F(40),
            "extended": 0,
        },
        {
            "normal": KEY_F(5),
            "shift": KEY_F(17),
            "control": KEY_F(29),
            "alt": KEY_F(41),
            "extended": 0,
        },
        {
            "normal": KEY_F(6),
            "shift": KEY_F(18),
            "control": KEY_F(30),
            "alt": KEY_F(42),
            "extended": 0,
        },
        {
            "normal": KEY_F(7),
            "shift": KEY_F(19),
            "control": KEY_F(31),
            "alt": KEY_F(43),
            "extended": 0,
        },
        {
            "normal": KEY_F(8),
            "shift": KEY_F(20),
            "control": KEY_F(32),
            "alt": KEY_F(44),
            "extended": 0,
        },
        {
            "normal": KEY_F(9),
            "shift": KEY_F(21),
            "control": KEY_F(33),
            "alt": KEY_F(45),
            "extended": 0,
        },
        {
            "normal": KEY_F(10),
            "shift": KEY_F(22),
            "control": KEY_F(34),
            "alt": KEY_F(46),
            "extended": 0,
        },
        {
            "normal": KEY_F(11),
            "shift": KEY_F(23),
            "control": KEY_F(35),
            "alt": KEY_F(47),
            "extended": 0,
        },
        {
            "normal": KEY_F(12),
            "shift": KEY_F(24),
            "control": KEY_F(36),
            "alt": KEY_F(48),
            "extended": 0,
        },
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {
            "normal": 0x5B,
            "shift": 0x7B,
            "control": 0x1B,
            "alt": ALT_LBRACKET,
            "extended": 0,
        },
        {
            "normal": 0x5C,
            "shift": 0x7C,
            "control": 0x1C,
            "alt": ALT_BSLASH,
            "extended": 0,
        },
        {
            "normal": 0x5D,
            "shift": 0x7D,
            "control": 0x1D,
            "alt": ALT_RBRACKET,
            "extended": 0,
        },
        {"normal": 0, "shift": 0, "control": 0x27, "alt": ALT_FQUOTE, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
    ]

    ext_kptab = [
        {"normal": 0, "shift": 0, "control": 0, "alt": 0, "extended": 0},
        {
            "normal": PADENTER,
            "shift": SHF_PADENTER,
            "control": CTL_PADENTER,
            "alt": ALT_PADENTER,
            "extended": 0,
        },
        {
            "normal": PADSLASH,
            "shift": SHF_PADSLASH,
            "control": CTL_PADSLASH,
            "alt": ALT_PADSLASH,
            "extended": 0,
        },
        {
            "normal": KEY_PPAGE,
            "shift": KEY_SPREVIOUS,
            "control": CTL_PGUP,
            "alt": ALT_PGUP,
            "extended": 0,
        },
        {
            "normal": KEY_NPAGE,
            "shift": KEY_SNEXT,
            "control": CTL_PGDN,
            "alt": ALT_PGDN,
            "extended": 0,
        },
        {
            "normal": KEY_END,
            "shift": KEY_SEND,
            "control": CTL_END,
            "alt": ALT_END,
            "extended": 0,
        },
        {
            "normal": KEY_HOME,
            "shift": KEY_SHOME,
            "control": CTL_HOME,
            "alt": ALT_HOME,
            "extended": 0,
        },
        {
            "normal": KEY_LEFT,
            "shift": KEY_SLEFT,
            "control": CTL_LEFT,
            "alt": ALT_LEFT,
            "extended": 0,
        },
        {
            "normal": KEY_UP,
            "shift": KEY_SUP,
            "control": CTL_UP,
            "alt": ALT_UP,
            "extended": 0,
        },
        {
            "normal": KEY_RIGHT,
            "shift": KEY_SRIGHT,
            "control": CTL_RIGHT,
            "alt": ALT_RIGHT,
            "extended": 0,
        },
        {
            "normal": KEY_DOWN,
            "shift": KEY_SDOWN,
            "control": CTL_DOWN,
            "alt": ALT_DOWN,
            "extended": 0,
        },
        {
            "normal": KEY_IC,
            "shift": KEY_SIC,
            "control": CTL_INS,
            "alt": ALT_INS,
            "extended": 0,
        },
        {
            "normal": KEY_DC,
            "shift": KEY_SDC,
            "control": CTL_DEL,
            "alt": ALT_DEL,
            "extended": 0,
        },
        {
            "normal": PADSLASH,
            "shift": SHF_PADSLASH,
            "control": CTL_PADSLASH,
            "alt": ALT_PADSLASH,
            "extended": 0,
        },
    ]

    save_press = 0
    left_key = 0
    special = False

    def is_special():
        return special

    def get_key_count(KEV: KEY_EVENT_RECORD):
        global save_press, left_key
        num_keys = 0

        vk: int = KEV.wVirtualKeyCode
        if KEV.bKeyDown:
            save_press = 0

            if vk == VK_CAPITAL or vk == VK_NUMLOCK or vk == VK_SCROLL:
                pass
            elif vk == VK_SHIFT or vk == VK_CONTROL or vk == VK_MENU:
                save_press = vk
                if vk == VK_SHIFT:
                    left_key = user32.GetKeyState(VK_LSHIFT)
                if vk == VK_CONTROL:
                    left_key = user32.GetKeyState(VK_LCONTROL)
                if vk == VK_MENU:
                    left_key = user32.GetKeyState(VK_LMENU)
            else:
                if KEV.uChar.UnicodeChar or not (
                    user32.MapVirtualKeyW(vk, 2) & 0x80000000
                ):
                    num_keys = KEV.wRepeatCount
        else:
            if (vk == VK_MENU and KEV.uChar.UnicodeChar != 0) or (
                (vk == VK_SHIFT or vk == VK_CONTROL or vk == VK_MENU)
                and vk == save_press
            ):
                save_press = 0
                num_keys = 1

        return num_keys

    def process_key_event(KEV: KEY_EVENT_RECORD):
        global special
        key: int = ord(KEV.uChar.UnicodeChar)
        vk: int = KEV.wVirtualKeyCode
        state: int = KEV.dwControlKeyState

        idx = 0
        enhanced = False

        special = True

        if vk == VK_SHIFT:
            return KEY_SHIFT_L if (left_key & 0x8000 != 0) else KEY_SHIFT_R

        if vk == VK_CONTROL:
            return KEY_CONTROL_L if (left_key & 0x8000 != 0) else KEY_CONTROL_R

        if vk == VK_MENU:
            if key != 0:
                return KEY_ALT_L if (left_key & 0x8000 != 0) else KEY_ALT_R

        if key and (
            (state & LEFT_ALT_PRESSED != 0) or (state & RIGHT_ALT_PRESSED == 0)
        ):
            if kptab[vk]["extended"] == 0:
                special = False
                return key

        if (state & ENHANCED_KEY != 0) and (kptab[vk]["extended"] != 999):
            enhanced = True
            idx = kptab[vk]["extended"]
        else:
            enhanced = False
            idx = vk
        if state & SHIFT_PRESSED != 0:
            key = ext_kptab[idx]["shift"] if enhanced else kptab[idx]["shift"]

        elif state & (LEFT_CTRL_PRESSED | RIGHT_CTRL_PRESSED):
            key = ext_kptab[idx]["control"] if enhanced else kptab[idx]["control"]

        elif state & (LEFT_ALT_PRESSED | RIGHT_ALT_PRESSED):
            key = ext_kptab[idx]["alt"] if enhanced else kptab[idx]["alt"]

        else:
            key = ext_kptab[idx]["normal"] if enhanced else kptab[idx]["normal"]

        if key < KEY_CODE_YES:
            special = False

        return key
