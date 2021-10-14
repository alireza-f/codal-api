# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3 as sql


class CodalPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sql.connect('codal_dps.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS dps_table""")

        self.curr.execute("""CREATE TABLE dps_table(
            name TEXT,
            dps INTEGER,
            date TEXT
            )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""INSERT INTO dps_table values(?, ?, ?)""", (
            item['name'],
            item['dps'],
            item['date']
        ))
        self.conn.commit()
