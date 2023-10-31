if __name__ == "__main__":
    from common import AttrDict, Parser
else:
    from .common import AttrDict, Parser


class AnimeParser(Parser):
    def __init__(self, contents: str):
        super().__init__(contents)
        self.id = None
        self.name = None
        self.logo_url = None

    def handle_start(self, tag: str, attrs: AttrDict):
        if attrs.get("id") == "movie_id" and attrs.get("value") is not None:
            self.id = attrs["value"]
            return

        if (
            tag == "img"
            and self.curent_tag.parent.attrs.get("class") == "anime_info_body_bg"
        ):
            self.logo_url = attrs.get("src")

    def handle_data(self, data: str):
        data = data.strip()
        if data == "":
            return

        if (
            self.curent_tag.tag == "h1"
            and self.curent_tag.parent.attrs.get("class") == "anime_info_body_bg"
        ):
            self.name = data
