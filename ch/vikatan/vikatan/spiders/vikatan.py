import re
import bs4
import pdb
import datetime
import urllib
from pprint import pprint, pformat
from w3lib.html import remove_tags, remove_tags_with_content

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from vikatan.items import Item

from  dateutil.parser import parse as fromisoformat

class VikatanSpider(CrawlSpider):
    name = 'vikatan_spider'
    allowed_domains = ['vikatan.com']
    start_urls = ['http://vikatan.com/']

    rules = [
        
        Rule(
            LinkExtractor(
                allow=[r'\w+/\w+/\w+'],

            ),
            callback='parse_news',
            follow=True,
        ),

    ]

    errored_count = 0

    def _make_date(self, date_string):
        return fromisoformat(date_string)
        
    def parse_news(self, response):

        if self.errored_count and self.errored_count % 20 == 0:
            print('errored_count:{}'.format(self.errored_count))
            pprint(self.crawler.stats.get_stats())

        try:
            selector     = response.xpath(
                '//article'
            )
            
            if not selector:
                return
            
            item = Item()

            item['url']        = response.url                                                      
            item['filename']   = response.url.split('/')[-1].split('?')[0]                         
            item['breadcrumb'] = response.xpath(
                '//h2[@id="system-breadcrumb"]/ol[@class="breadcrumb"]/li/a/text()'
            ).extract()
            
            author = selector.xpath(
                '//span[contains(@class,"contributor-name")]/text()'
            )

            if author:
                item['author'] = [i.extract().strip() for i in author]
            else:
                item['author'] = []
            
            item['date']    = selector.xpath(
                '//span[contains(@class,"published")]/time/@datetime'
            ).extract()[0].strip()

            item['date']    =  self._make_date(item['date'])

            item['content'] = selector.xpath(
                '//div[contains(@class, "story-element-text")]'
            ).extract()
            
            item['content'] = '\n\n'.join([
                remove_tags(remove_tags_with_content(content, ('script', ))).strip()
                for content in item['content']
            ])
            
            item['title']   = selector.xpath(
                '//h1[contains(@class,"headline")]/text()'
            )[0].extract().strip()
            
            item['tags']    = selector.xpath(
                '//ul[contains(@class, "tags")]//a/text()'
            ).extract()

            
            if item['content']:
                yield item

        except KeyboardInterrupt:
            print('got killed by the keyboard :(')
            raise KeyboardInterrupt
        except:
            self.errored_count += 1
            self.logger.exception(urllib.parse.unquote(response.url))
            
