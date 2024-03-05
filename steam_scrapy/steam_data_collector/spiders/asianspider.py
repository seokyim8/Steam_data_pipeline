from typing import Iterable
import scrapy


class AsianspiderSpider(scrapy.Spider):
    name = "asian"
    allowed_domains = ["store.steampowered.com"]
    urls = ["https://store.steampowered.com/"]

    def start_requests(self) -> Iterable[scrapy.Request]:
        for url in self.urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        print(response)
