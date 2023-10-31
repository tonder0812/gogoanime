import sys
from typing import Generator

widths = {
    31: 0,
    126: 1,
    159: 0,
    687: 1,
    710: 0,
    711: 1,
    727: 0,
    733: 1,
    879: 0,
    1154: 1,
    1161: 0,
    4347: 1,
    4447: 2,
    7467: 1,
    7521: 0,
    8369: 1,
    8426: 0,
    9000: 1,
    9002: 2,
    11021: 1,
    12350: 2,
    12351: 1,
    12438: 2,
    12442: 0,
    19893: 2,
    19967: 1,
    55203: 2,
    63743: 1,
    64106: 2,
    65039: 1,
    65059: 0,
    65131: 2,
    65279: 1,
    65376: 2,
    65500: 1,
    65510: 2,
    120831: 1,
    262141: 2,
    1114109: 1,
}

ALLOWED_NON_PRINTABLE_CHARS = {"\n", "\t"}
NOPRINT_TRANS_TABLE = {
    i: None
    for i in range(0, sys.maxunicode + 1)
    if not chr(i).isprintable() and chr(i) not in ALLOWED_NON_PRINTABLE_CHARS
}


def remove_control_chars(s: str):
    return s.translate(NOPRINT_TRANS_TABLE)


def get_width(char: str) -> int:
    x = ord(char)
    if x in NOPRINT_TRANS_TABLE:
        return -1
    if x == 0x0E or x == 0x0F:
        return 0
    for code, width in widths.items():
        if x <= code:
            return width
    return 1


tabsize = 8


def set_tabsize(x: int):
    global tabsize
    tabsize = x


def length(text: str) -> int:
    total: int = 0
    for c in text:
        if c == "\t":
            total += tabsize - (total % tabsize)
        else:
            total += get_width(c)
    return total


def cut_unicode(text: str, width: int) -> tuple[str, str]:
    res: str = ""
    res_len: int = 0
    safe = text
    for c in safe:
        tab = 0
        if c == "\t":
            tab = tabsize - (res_len % tabsize)
            res_len += tab
        else:
            res_len += get_width(c)
        if res_len >= width:
            break
        if c == "\t":
            res += " " * tab
        else:
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


def split_lines_width(
    text: str, width: int, height: int, start_line: int
) -> Generator[str, None, None]:
    current_line = 0
    for line in text.split("\n"):
        while length(line) >= width:
            current_line += 1
            s, line = cut_unicode(line, width)
            if current_line > start_line:
                if current_line - start_line >= height:
                    return
                yield s
        current_line += 1
        if current_line > start_line:
            if current_line - start_line >= height:
                return
            s, line = cut_unicode(line, width)
            yield s
