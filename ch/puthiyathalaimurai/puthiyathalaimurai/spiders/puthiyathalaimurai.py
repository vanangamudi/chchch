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
from puthiyathalaimurai.items import Item

from  dateutil.parser import parse as fromisoformat

def strip_remove_dupes_empties(llist):
    llist = [i.strip() for i in llist if i.strip()]
    return list(set(llist))

class PuthiyaThalaimuraiSpider(CrawlSpider):
    name = 'puthiyathalaimurai_spider'
    allowed_domains = ['puthiyathalaimurai.com']
    start_urls = ['http://puthiyathalaimurai.com']

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


        selectors     = response.xpath(
            '//section[contains(@class, "pt-main-news-section")]'
        )

        for selector in selectors[:1]:
            try:		
		
                item = Item()
                
                item['url']        = response.url                                                      
                item['filename']   = response.url.split('/')[-1].split('?')[0]                         

                breadcrumb = response.xpath(
                    '//div/ul[@class="breadcrumbs-list"]/li[@class="breadcrumbs-list-elmnts"]/a/text()'
                ).extract()

                item['breadcrumb'] = strip_remove_dupes_empties(breadcrumb)
                
                author_date = selector.xpath('.//div[@class="article-author"]')
                author = author_date.xpath(
                    './/a/text()'
                ).extract()
                
                item['author'] = strip_remove_dupes_empties(author)
                    
                item['date']    = author_date.xpath(
                    './/span[contains(@class,"pull-right")]/text()'
                ).extract()[0]
                
                item['date']    =  self._make_date(item['date'])
                
                item['content'] = selector.xpath(
                    './/div[contains(@class, "single-news-desc-panel")]'
                ).extract()
                
                item['content'] = '\n\n'.join([
                    remove_tags(remove_tags_with_content(content, ('script', ))).strip()
                    for content in item['content']
                ])
                
                item['title']   = selector.xpath(
                    './/h1[contains(@class,"main-image-header")]/text()'
                )[0].extract().strip()
                
                item['tags']    = selector.xpath(
                    './/ul[contains(@class, "tags")]//a/text()'
                ).extract()

            
                yield item
                
            except KeyboardInterrupt:
                print('got killed by the keyboard :(')
                raise KeyboardInterrupt
            except:
                self.errored_count += 1
                self.logger.exception(urllib.parse.unquote(response.url))
                pdb.set_trace()
                
