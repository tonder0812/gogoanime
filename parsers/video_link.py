import base64
import re

if __name__ == "__main__":
    from common import Parser
else:
    from .common import Parser


class VideoLinkParser(Parser):
    def __init__(self, contents: str):
        super().__init__(contents)
        self.download_link = None
        self.resolution = None
        self.best_resolution = 0

    def handle_data(self, data: str):
        data = data.strip()
        if data == "":
            return
        if (
            self.curent_tag.tag == "a"
            and self.curent_tag.parent.attrs.get("class") == "cf-download"
        ):
            dim = data.split("x")
            if len(dim) != 2:
                return

            resolution = int(dim[0]) * int(dim[1])
            if resolution > self.best_resolution:
                self.download_link = self.curent_tag.attrs.get("href")
                if self.download_link is not None:
                    self.download_link = self.download_link.replace(
                        "gredirect.info", "ggredi.info"
                    )
                self.best_resolution = resolution
                self.resolution = data


class VideoProviderLinkParser(Parser):
    def __init__(self, contents: str):
        super().__init__(contents)
        self.link: str | None = None

    def handle_data(self, data: str) -> None:
        data = data.strip()
        if (
            self.curent_tag.tag == "option"
            and data.startswith("SUB")
            and data.endswith("Moon")
        ):
            encoded = self.curent_tag.attrs.get("value")
            assert encoded is not None
            matches = re.findall('src="(.*?)"', base64.b64decode(encoded).decode())
            assert len(matches) == 1
            self.link = matches[0]
            assert isinstance(self.link, str)
            if self.link.startswith("//"):
                self.link = "https:" + self.link
