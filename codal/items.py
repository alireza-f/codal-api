# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CodalItem(scrapy.Item):
    name = scrapy.Field()
    dps = scrapy.Field()
    date = scrapy.Field()
