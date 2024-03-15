FROM python:3.12

# Setting Timezone:
ENV TZ="America/New_York"


# Install other Python dependencies:
RUN pip install --upgrade pip setuptools wheel
RUN pip install scrapy 
RUN pip install selenium
RUN pip install apscheduler
RUN pip install pymysql

# Install Chrome
RUN apt-get update -y
RUN apt -f install -y
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

WORKDIR /usr/src/app

# Copy project code from local host to Docker container:
COPY . .


# Crawling action!
CMD ["python3", "./main.py"]