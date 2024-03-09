from typing import Iterable
import scrapy
from pathlib import Path
import json
import re
from datetime import date
import time
from selenium import webdriver


class AsianspiderSpider(scrapy.Spider):
    name = "asian"
    allowed_domains = ["store.steampowered.com"]
    urls = ["https://store.steampowered.com/search/?sort_by=Released_DESC&supportedlang=english"] # Steam link for new releases
    save_file = "fetched_info.json" # Used for debugging
    scroll_freq = 0 # TODO: CHANGE TO DESIRED NUMBER LATER!

    def start_requests(self) -> Iterable[scrapy.Request]:
        """Returns scraped data from each specified url after initializing webscraping request to Steam. Assigns a chrome webdriver to self.driver."""
        # Resetting result file for webscraping process
        with Path(self.save_file).open("w") as f:
            json.dump([], f)

        # Preparing for scrolling
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--profile-directory=Default')
        self.driver = webdriver.Chrome(options = options)

        for url in self.urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        """Returns scraped data from a specific starting url. Handles pages with infinite-scroll mechanisms through the usage of selenium."""
        # Scrolling:
        self.driver.get(response.url)
        for i in range(self.scroll_freq):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1) # Waiting for page to load
        selector = scrapy.Selector(text = self.driver.page_source)

        links = selector.css("div[id='search_resultsRows'] a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback = self.parse_game)
        self.driver.quit()
    
    def parse_game(self, response):
        """Returns data for each individual item in the list of new steam game releases. Transfers fetched data to self.save_file in .json format."""
        # This function includes the process of filtering out non-games (music dlc, for instance) and unreleased games

        header_grid_content = response.css("div[id='gameHeaderImageCtn'] div.grid_content a::text").getall()
        if len(header_grid_content) < 2: # Checks whether it is a game page or something else
            return None

        genre = response.css("div[id='genresAndManufacturer'] span a::text").get()
        if genre == None:
            genre = "None"

        num_of_reviews = response.css("div[id='review_histogram_rollup_section'] div.summary_section span::text").get()
        if num_of_reviews == None:
            num_of_reviews = 0

        price = response.css("div.game_purchase_action_bg div.game_purchase_price.price::text").get()
        if price == None:
            price = response.css("div.game_purchase_action_bg div.discount_block.game_purchase_discount div.discount_final_price::text").get()
        if price == None:
            # Means game has no price since it has not been released yet
            return None
        price = price.strip()

        review_summary = response.css("span.game_review_summary::text").get()
        review_count = response.css("div.user_reviews_summary_bar span::text").getall()

        if review_summary == None or review_count == None or len(review_count) < 2:
            review_summary = "None"
            review_count = 0
        else:
            review_count = review_count[1].replace("(","").replace(")","").split(" ")[0]

        fetched = {"name": response.css("div[id='appHubAppName_responsive']::text").get(),
               "developer": header_grid_content[0], "publisher": header_grid_content[1], 
               "release_date": response.css("div[id='gameHeaderImageCtn'] div.grid_content.grid_date::text").get().strip(),
               "genre": genre.strip(), "number_of_reviews": review_count, "url": response.url,
               "app_id": re.split("/",  response.url)[4], "price": price, "review_summary": review_summary,
               "fetched_date": str(date.today())}
        
        arr = []
        with Path(self.save_file).open("r") as f:
            arr = json.load(f)

        with Path(self.save_file).open("w") as f:
            arr.append(fetched)
            json.dump(arr, f)

        yield fetched


        # Note:
        # Possible plots to generate:
        # percentage of free to play games per genre, statistics per genre, user review positivity per genre, user review count per genre, 
        # which genre is popular nowadays, how many new games today

        # The ones that need data over a time period:
        # new releases' price trend, genre releases' price trend per genre, new release's user review posivitiy/number of reviews trend,
        # the nubmer of new releases per day trend

        # Types of data we need to record:
        # game_id, price, genre, review count, review positivity, record_fetched_date

        # API for retreiving concurrent number of players for a steam game:
        # https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=730

        # Question:
        # Do I need ENV varaible for AWS EC2 in case their devices do not have chrome? (since I use chrome for the selenium part of my code)