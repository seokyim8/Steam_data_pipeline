# TODO: Create a "scheduler" that takes care of automatically activating scrapy crawling functionalities to regularly scrape 
# new releases' data from steam. 

import time
import os
import subprocess
from datetime import date, datetime

SPIDER_NAME = 'asian'

def run_scraper():
    """Runs the spider to scrape from Steam the data relating to newly released games."""
    subprocess.run(['scrapy', 'crawl', SPIDER_NAME])

# Main Function
if __name__ == "__main__":
    run_scraper()