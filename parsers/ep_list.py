if __name__ == "__main__":
    from common import Parser
else:
    from parsers.common import Parser


class EpListParser(Parser):
    def __init__(self, contents: str):
        super().__init__(contents)
        self.links: dict[str, str] = {}

    def handle_data(self, data: str):
        data = data.strip()
        if data == "":
            return

        if (
            self.curent_tag.tag == "div"
            and self.curent_tag.attrs.get("class") == "name"
        ):
            link = self.curent_tag.parent.attrs.get("href")
            assert link is not None
            self.links[data] = link.strip()
