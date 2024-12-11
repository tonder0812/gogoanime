if __name__ == "__main__":
    from common import AttrDict, Parser
else:
    from .common import AttrDict, Parser


class AnimeParser(Parser):
    def __init__(self, contents: str):
        super().__init__(contents)
        self.name = None
        self.logo_url = None

    def handle_start(self, tag: str, attrs: AttrDict):
        className = self.curent_tag.parent.attrs.get("class")
        if tag == "img" and className is not None and className.find("thumb") != -1:
            self.logo_url = attrs.get("src")

    def handle_data(self, data: str):
        data = data.strip()
        if data == "":
            return

        if (
            self.curent_tag.tag == "h1"
            and self.curent_tag.attrs.get("class") == "entry-title"
        ):
            self.name = data
