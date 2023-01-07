if __name__ == "__main__":
    from common import Parser
else:
    from .common import Parser


class VideoLinkParser(Parser):
    def __init__(self, contents: str):
        super().__init__(contents)
        self.downloadLink = None

    def handle_data(self, data: str):
        data = data.strip()
        if data == "":
            return
        if (self.curent_tag.tag == "a"
                and self.curent_tag.parent.attrs.get("class") == "cf-download"
                and data in ("1280x720", "1920x1080", "2580x1080", "3840x2160")):
            self.downloadLink = self.curent_tag.attrs.get("href")
