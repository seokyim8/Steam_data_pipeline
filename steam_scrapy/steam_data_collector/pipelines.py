# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter
import mysql.connector
import secrets


class SteamDataCollectorPipeline:
    """Initializes connection to the AWS RDS MYSQL instance."""
    def open_spider(self, spider):
        # self.db = mysql.connector.connect(
        #     host = secrets.__path__,
        #     user = secrets.__path__,
        #     password = secrets.__path__ 
        # )
        # self.db.disconnect()
        pass

    """Process the scraped data from Steam and upsert to the MYSQL table."""
    def process_item(self, item, spider):
        return item
