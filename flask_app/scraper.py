import subprocess
import time
from threading import Thread

def scraper():
    while True:
        spider_name = 'gradient'
        subprocess.check_output(
            ['scrapy', 'crawl', spider_name])
        time.sleep(60*60)

Thread(target=scraper).start()