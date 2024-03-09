# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter
import secrets # The secret file that is included in .gitignore
import pymysql
import sshtunnel

class SteamDataCollectorPipeline:
    def open_spider(self, spider):
        """Initializes connection to the AWS RDS MYSQL instance."""

        self.db = pymysql.connect(
            host = secrets.RDS_ENDPOINT,
            port = secrets.RDS_PORT,
            user = secrets.RDS_USER,
            password = secrets.RDS_PASSWORD
        )
        self.cur = self.db.cursor()
    
    def process_item(self, item, spider):
        """Process the scraped data from Steam and upsert to the MYSQL table."""
        return item
    
    def close_spider(self, spider):
        self.db.close()

## DEBUGGING:

if __name__ == "__main__":
    spidy = SteamDataCollectorPipeline()
    spidy.open_spider(None)
