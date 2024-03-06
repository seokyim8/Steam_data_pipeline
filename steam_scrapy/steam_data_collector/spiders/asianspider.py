from typing import Iterable
import scrapy
from pathlib import Path
import json



class AsianspiderSpider(scrapy.Spider):
    name = "asian"
    allowed_domains = ["store.steampowered.com"]
    urls = ["https://store.steampowered.com/search/?sort_by=Released_DESC&supportedlang=english"]
    save_file = "steam_new_releases_info.json"

    def start_requests(self) -> Iterable[scrapy.Request]:
        # Resetting result file for webscraping process
        with Path(self.save_file).open("w") as f:
            json.dump([], f)

        for url in self.urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        links = response.css("div[id='search_resultsRows'] a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback = self.parse_game)
    
    def parse_game(self, response):
        header_grid_content = response.css("div[id='gameHeaderImageCtn'] div.grid_content a::text").getall()
        if len(header_grid_content) < 2: # Checks whether it is a game page or something else
            return None

        genre = response.css("div[id='genresAndManufacturer'] span a::text").get()
        if genre == None:
            genre = "None"

        num_of_reviews = response.css("div[id='review_histogram_rollup_section'] div.summary_section span::text").get()
        if num_of_reviews == None:
            num_of_reviews = 0

        fetched = {"name": response.css("div[id='appHubAppName_responsive']::text").get(),
               "developer": header_grid_content[0], "publisher": header_grid_content[1], 
               "release_date": response.css("div[id='gameHeaderImageCtn'] div.grid_content.grid_date::text").get().strip(),
               "genre": genre.strip(), "number_of_reviews": num_of_reviews}
        
        arr = []
        with Path(self.save_file).open("r") as f:
            arr = json.load(f)

        with Path(self.save_file).open("w") as f:
            arr.append(fetched)
            json.dump(arr, f)

        yield fetched