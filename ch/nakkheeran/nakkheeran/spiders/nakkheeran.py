import re
import bs4
import pdb
import datetime
from w3lib.html import remove_tags, remove_tags_with_content

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from nakkheeran.items import Item

class NakkheeranSpider(CrawlSpider):
    name = 'nakkheeran_spider'
    allowed_domains = ['nakkheeran.in']
    start_urls = ['http://nakkheeran.in/']

    rules = [
        
        Rule(
            LinkExtractor(allow=[r'/.*']),
            callback='parse_news',
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
        
    def parse_news(self, response):

        selector     = response.xpath('//div[@id="page-main-content"]')
        if selector:
            item = Item()

            item['url']        = response.url                                                      
            item['filename']   = response.url.split('/')[-1].split('?')[0]                         
            item['breadcrumb'] = response.xpath('//h2[@id="system-breadcrumb"]/ol[@class="breadcrumb"]/li/a/text()').extract()
            

            item['author']  = selector.xpath('string(//div[contains(@class,"node_cus_editor")])')[0].extract().strip()
            item['date']    = selector.xpath('//span[contains(@class,"post-created")]/text()')[0].extract().strip()
            item['date']    =  self._make_date(item['date'])
            
            item['content'] = selector.xpath('//div[contains(@class, "node__content")]')[0].extract()
            item['content'] = remove_tags(
                remove_tags_with_content(item['content'], ('script', ))).strip()
            
            item['title']   = selector.xpath('//h1[contains(@class,"title")]/text()')[0].extract().strip()
            item['tags']    = selector.xpath('//div[contains(@class, "field--name-field-tags")]//a/text()').extract()


            if item['content']:
                yield item
