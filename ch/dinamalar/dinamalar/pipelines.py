# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import re
import json
import datetime

import pymongo

from dinamalar.settings import DATA_DIR
from dinamalar.settings import (MONGODB_COLLECTION, MONGODB_DB,
                             MONGODB_SERVER, MONGODB_PORT)

class MongoDBPipeline(object):

    def __init__(self):
        self.connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )

        self.setup_db()
        
    def setup_db(self):
        self.db = self.connection[MONGODB_DB]
        self.collection = self.db[MONGODB_COLLECTION]

        self.collection.create_index([
            ("url", -1)
        ])

        
    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")

        
        retval = self.collection.replace_one(
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
    
    
