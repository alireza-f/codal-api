import subprocess
import time


def scraper():
    while True:
        spider_name = "gradient"
        time.sleep(4*60)
        subprocess.check_output(
            ['scrapy', 'crawl', spider_name, "-O", "output.json"])
