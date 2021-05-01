# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from hindu_tamil.settings import DATA_DIR
import os
import re
import json
import datetime

import pymongo

from hindu_tamil.settings import (MONGODB_COLLECTION, MONGODB_DB,
                             MONGODB_SERVER, MONGODB_PORT)

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        db = connection[MONGODB_DB]
        self.collection = db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.replace_one(
            {'url' : item['url'] },
            dict(item),
            upsert = True
        )
        
        return item


    
class Pipeline(MongoDBPipeline):
    month_mapping = {'jan': 1,
                     'feb': 2,
                     'mar': 3,
                     'apr': 4,
                     'may': 5,
                     'jun': 6,
                     'jul': 7,
                     'aug': 8,
                     'sep': 9,
                     'oct': 10,
                     'nov': 11,
                     'dec': 12
    }
    def __init__(self):
        super().__init__()
        
    def makedate(self, date):
        match = re.match('(\d+) (\w{3}) (\d{4})', date)
        if match:
            day, month, year = match.groups()
            day, month, year = int(day), self.month_mapping[month.lower()], int(year)
        else:
            day, month, year = 0, 0 ,0

        return (year, month, day)

    def process_item(self, item, spider):

        item['date'] = self.makedate(item['date'])
        
        return super().process_item(item, spider)
    
    
