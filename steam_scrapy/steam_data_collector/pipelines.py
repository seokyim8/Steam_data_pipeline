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
        # self.cur.execute("SELECT name from temp;")
        # result = self.cur.fetchall()
        # for row in result:
        #     print(row)
    
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

        if item == None:
            return item

         # Cleaning Process of individual data entries: 
        item["release_date"] = format_release_date(item["release_date"])
        item["price"] = item["price"].strip().replace("$","")


        # TODO: I NEED TO CONVERT EVERYTHING TO STRING VALUES AND ALSO WRAP STRING FORMATS WITH SINGLE QUOTES
        self.cur.execute("INSERT IGNORE INTO new_games VALUES("
                         + item["name"] + ","
                         + item["developer"] + ","
                         + item["publisher"] + ","
                         + item["release_date"] + ","
                         + item["genre"] + ","
                         + item["number_of_reviews"] + ","
                         + item["url"] + ","
                         + item["app_id"] + ","
                         + item["price"] + ","
                         + item["review_summary"] + ","
                         + item["fetched_date"] + ");")

        return item
    
    def close_spider(self, spider):
        self.db.close()
