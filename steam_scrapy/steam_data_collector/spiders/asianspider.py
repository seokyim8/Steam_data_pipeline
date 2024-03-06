from typing import Iterable
import scrapy
from pathlib import Path


class AsianspiderSpider(scrapy.Spider):
    name = "asian"
    allowed_domains = ["store.steampowered.com"]
    urls = ["https://store.steampowered.com/explore/new/"]
    save_file = "steam_new_releases.html"

    def start_requests(self) -> Iterable[scrapy.Request]:
        for url in self.urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        Path(self.save_file).write_bytes(response.body)
