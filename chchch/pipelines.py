# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from chchch.settings import DATA_DIR
import os
import re
import json
import datetime

def mkdir_if_exist_not(name):
    if not os.path.isdir(name):
        return os.makedirs(name, exist_ok=True)

class HindutamilPipeline:
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

    def makepath(self, date):
        path = '{}{}{}{}{}{}{}{}'.format(DATA_DIR, os.sep,
                                         date[0], os.sep,
                                         date[1], os.sep,
                                         date[2], os.sep)
        mkdir_if_exist_not(path)
        yield path

    def makedate(self, date):
        match = re.match('(\d+) (\w{3}) (\d{4})', date)
        if match:
            day, month, year = match.groups()
            day, month, year = int(day), self.month_mapping[month.lower()], int(year)
        else:
            day, month, year = 0, 0 ,0

        yield (year, month, day)

    def process_item(self, item, spider):

        item['date'] = self.makedate(item['date'])

        path = self.makepath(item['date'])
        with open('{}{}{}'.format(path,
                                  os.sep,
                                  item['filename'].replace('.html', '.json')),
                  'w',
                  encoding='utf-8'
                  ) as f:
            json.dump(dict(item), f, ensure_ascii=False)

        yield item

    
