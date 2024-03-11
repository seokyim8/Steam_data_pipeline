Creator: Seok Yim (Noah)
<br><br>
<strong>Do you want to be the PIONEER of soon-to-POP-OFF games? Then you're gonna like this...</strong>
<br><br>
Title: <strong>Steam Data Pipeline</strong>
<br>
### Project Summary: 
A data pipeline that regularly scrapes, cleans, stores, and publishes data for newly released games on Steam. The data visualization is taken care of by Apache Superset (publicly accessible).
<br><br>
*** Preview ***<br>
<img width="1680" alt="DASHBOARD" src="https://github.com/seokyim8/Steam_data_pipeline/assets/49558316/3a67cccb-c57c-439a-9f32-b2d0e6acaad2">
<br>
Website link:<br>
http://18.212.126.33:8080/superset/dashboard/1/?standalone=3&show_filters=1
<br><br>
Authentication for anonymous users (Anyone can view it with these credentials):<br>
ID: public<br>
password: public<br>
<br>
## Description:
I frequently saw websites/projects with Steam-related data for popular(top 100) games but never saw one primarily focused on new releases on Steam. Thus, I decided to make one myself.
### Technologies Used:
- Python, MYSQL, AWS(EC2, RDS), Docker, Scrapy, Apache Superset, Selenium
### Steps Taken:
1) Created a Scrapy project that scrapes data from the official Steam website(https://store.steampowered.com/search/?sort_by=Released_DESC&supportedlang=english).
2) Added selenium to deal with infinite scrolling. Created a Python scheduler with Apscheulder along with Python asyncio.
3) Launched an EC2 and RDS instance, each for persisting the program and running the MYSQL database, respectively.
4) Created a Docker image that downloads the Python dependencies along with the Chrome browser.
5) On EC2, initialized the containerized project along with the containerized Apache Superset image.
6) Made the dashboard publicly available.

<h3>Final Product:</h3>
- A dashboard/BI tool that updates every day at 7:30 am EST with 1,000 entries from Steam.
- Contains visual expressions of the data that facilitate gamers/YouTubers/companies in understanding the latest trends in games.
