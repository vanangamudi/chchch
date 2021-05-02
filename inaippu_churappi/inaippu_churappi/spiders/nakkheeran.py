import re
import bs4
import pdb
import datetime
import urllib
from w3lib.html import remove_tags, remove_tags_with_content

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from inaippu_churappi.items import InaippuChurappiItem as Item
class NakkheeranSpider(CrawlSpider):
    name = 'nakkheeran'
    allowed_domains = ['nakkheeran.in']
    start_urls = ['http://nakkheeran.in/']

    rules = [
        
        Rule(
            LinkExtractor(allow=[r'/.*']),
            callback='parse_link',
            follow=True,
        ),

    ]


    def _make_date(self, date_string):
        # example: "Published on 01/05/2021 (19:55) | Edited on 01/05/2021 (20:13)""
        pattern = r'.* Edited on (\d+)/(\d+)/(\d+) .*'
        match = re.search(pattern, date_string)
        if match:
            day, month, year = match.groups()
            day, month, year = map(int, [day, month, year])
            return datetime.datetime(year, month, day)
        else:
            return datetime.datetime(1, 1, 1)
        
    def parse_link(self, response):
        item = Item()
        item['url'] = urllib.parse.unquote(response.url)
        return item
