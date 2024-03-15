# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter
import pymysql
import os


class SteamDataCollectorPipeline:
    def open_spider(self, spider):
        """Initializes connection to the AWS RDS MYSQL instance."""

        self.db = pymysql.connect(
            host = os.environ.get("RDS_ENDPOINT"),
            port = int(os.environ.get("RDS_PORT")),
            user = os.environ.get("RDS_USER"),
            password = os.environ.get("RDS_PASSWORD"),
            database = "STEAM"
        )
        self.cur = self.db.cursor()
    
    def process_item(self, item, spider):
        """Process the scraped data for individual games from Steam and upsert to the MYSQL table."""
        def format_release_date(obj):
            month, date, year = obj.replace(",","").split(" ")

            match month:
                case "Jan":
                    month = "01"
                case "Feb":
                    month = "02"
                case "Mar":
                    month = "03"
                case "Apr":
                    month = "04"
                case "May":
                    month = "05"
                case "Jun":
                    month = "06"
                case "Jul":
                    month = "07"
                case "Aug":
                    month = "08"
                case "Sep":
                    month = "09"
                case "Oct":
                    month = "10"
                case "Nov":
                    month = "11"
                case "Dec":
                    month = "12"
            date = "0" + date if int(date) < 10 else date

            return "-".join([year, month, date])
        def format_price(obj):
            obj = obj.strip().replace("$","")
            if not obj.replace(".","").isdigit():
                obj = 0
            return obj

        if item == None:
            return item

         # Cleaning Process of individual data entries: 
        item["release_date"] = format_release_date(item["release_date"])
        item["price"] = format_price(item["price"])

        # Insert new entries
        self.cur.execute("INSERT IGNORE INTO new_games VALUES("
                         + f"'{item["name"]}',"
                         + f"'{item["developer"]}',"
                         + f"'{item["publisher"]}',"
                         + f"'{item["release_date"]}',"
                         + f"'{item["genre"]}',"
                         + f"{item["number_of_reviews"]},"
                         + f"'{item["url"]}',"
                         + f"{item["app_id"]},"
                         + f"{item["price"]},"
                         + f"'{item["review_summary"]}',"
                         + f"'{item["fetched_date"]}');")
        # Update overlapping items
        self.cur.execute("UPDATE new_games SET number_of_reviews = {}, review_summary = '{}', fetched_date = '{}' WHERE app_id={};".format(item["number_of_reviews"], item["review_summary"],item["fetched_date"], item["app_id"]))

        # Delete old items (entries whose release dates are at least 15 days behind)
        self.cur.execute("delete from new_games where release_date < date_sub(curdate(), interval 14 day);")
        self.db.commit()

        return item
    
    def close_spider(self, spider):
        self.db.close()
