import re
from html import unescape
from html.parser import HTMLParser
from types import TracebackType
from typing import Self

AttrDict = dict[str, str | None]


def attrs_to_dict(attrs: list[tuple[str, str | None]]) -> AttrDict:
    out: dict[str, str | None] = {}
    for attr in attrs:
        out[attr[0]] = attr[1]
    return out


class TagElem:
    INVALID: Self

    def __init__(self, tag: str, attrs: AttrDict, parent: Self | None = None):
        self.tag = tag
        self.attrs = attrs
        if parent is None:
            self.parent = self
        else:
            self.parent = parent


TagElem.INVALID = TagElem("???", {})


class Parser(HTMLParser):
    def __init__(self, contents: str) -> None:
        super().__init__()
        self.contents = contents
        self.parent_stack: list[TagElem] = []
        self.curent_tag = TagElem.INVALID

    def handle_start(self, tag: str, attrs: AttrDict):
        pass

    def handle_end(self, tag: str):
        pass

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = attrs_to_dict(attrs)
        self.parent_stack.append(TagElem(tag, attrs_dict, self.curent_tag))
        self.curent_tag = self.parent_stack[-1]
        self.handle_start(tag, attrs_dict)

    def handle_endtag(self, tag: str):
        self.handle_end(tag)
        self.parent_stack.pop()
        if len(self.parent_stack) > 0:
            self.curent_tag = self.parent_stack[-1]
        else:
            self.curent_tag = TagElem.INVALID

    def parse_starttag(self, i: int):
        self._HTMLParser__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self._HTMLParser__starttag_text = rawdata[i:endpos]

        # Now parse the data between i+1 and j into a tag and attrs
        attrs = []
        match = tagfind_tolerant.match(rawdata, i + 1)
        assert match, "unexpected call to parse_starttag()"
        k = match.end()
        self.lasttag = tag = match.group(1).lower()
        while k < endpos:
            m = attrfind_tolerant.match(rawdata, k)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif (
                attrvalue[:1] == "'" == attrvalue[-1:]
                or attrvalue[:1] == '"' == attrvalue[-1:]
            ):
                attrvalue = attrvalue[1:-1]
            if attrvalue:
                attrvalue = unescape(attrvalue)
            attrs.append((attrname.lower(), attrvalue))
            k = m.end()

        end = rawdata[k:endpos].strip()
        if end not in (">", "/>"):
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith("/>"):
            # XHTML-style empty tag: <span attr="value" />
            self.handle_startendtag(tag, attrs)
        elif end.endswith(">") and tag in frozenset(
            [
                "area",
                "base",
                "br",
                "col",
                "embed",
                "hr",
                "img",
                "input",
                "keygen",
                "link",
                "meta",
                "param",
                "source",
                "track",
                "wbr",
            ]
        ):
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
        return endpos

    def __enter__(self) -> Self:
        self.feed(self.contents)
        self.close()
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.parent_stack = []
        self.curent_tag = TagElem.INVALID


tagfind_tolerant = re.compile(r"([a-zA-Z][^\t\n\r\f />\x00]*)(?:\s|/(?!>))*")
attrfind_tolerant = re.compile(
    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*'
)
