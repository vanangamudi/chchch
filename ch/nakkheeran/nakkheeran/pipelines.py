# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from nakkheeran.settings import DATA_DIR
import os
import re
import json
import datetime

import pymongo

from nakkheeran.settings import (MONGODB_COLLECTION, MONGODB_DB,
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
    def __init__(self):
        super().__init__()
        
    def process_item(self, item, spider):

        return super().process_item(item, spider)
    
    
