if __name__ == "__main__":
    from common import Parser
else:
    from parsers.common import Parser


class EpListParser(Parser):
    def __init__(self, contents: str):
        super().__init__(contents)
        self.links: dict[str, str] = {}
        self.inlist = False
        self.curent_link: str | None = None

    def handle_start(self, tag: str, attrs: dict[str, str | None]):
        if tag == "div" and attrs.get("class") == "eplister":
            self.inlist = True
        if self.inlist and tag == "a":
            self.curent_link = attrs.get("href")

    def handle_end(self, tag: str):
        if (
            self.inlist
            and tag == "div"
            and self.curent_tag.attrs.get("class") == "eplister"
        ):
            self.inlist = False

    def handle_data(self, data: str):
        data = data.strip()
        if data == "":
            return

        if (
            self.curent_tag.tag == "div"
            and self.curent_tag.attrs.get("class") == "epl-num"
        ):
            assert self.curent_link is not None
            try:
                data = f"{float(data):g}"
            except:
                pass
            self.links[data] = self.curent_link.strip()
