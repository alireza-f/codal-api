# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class CodalPipeline:
    # def __init__(self):
    #     self.create_connection()
    #     self.create_table()

    # def create_connection(self):
    #     self.conn = sqlite3.connect('imgaes.db')
    #     self.curr = self.conn.cursor()

    # def create_table(self):
    #     self.curr.execute("""DROP TABLE IF EXISTS images_tb""")

    #     self.curr.execute("""CREATE TABLE images_tb(source text)""")

    # def save_images(self, item):
    #     self.curr.execute("""INSERT INTO images_tb VALUES(?)""",(
    #                                                                 item['src'],
    #                                                                             ))
    #     self.conn.commit()


    def process_item(self, item, spider):
        return item
