import time
import os
import subprocess
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
from datetime import date, datetime

SPIDER_NAME = 'asian'


def schedule_scraping():
    """Schedules the daily scraping process from Steam for the purpose of collecting new-releases related data."""
    def run_scraper():
        subprocess.run(['scrapy', 'crawl', SPIDER_NAME])
    
    # On startup, a single scraping process is initialized. After this point, the scraping occurs only on a regular basis.
    run_scraper()

    scheduler = AsyncIOScheduler()
    # At 7:30 am every morning, the RDS MYSQL instance will be updated with info pertaining to the newly released steam games.
    scheduler.add_job(func = run_scraper, 
                      trigger = CronTrigger(year = "*", month = "*", day = "*", hour = "7", minute = "30"))
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

# Main Function
if __name__ == "__main__":
    print("Successfully started running server.")
    schedule_scraping()