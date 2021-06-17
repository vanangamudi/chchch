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
from dinamalar.items import Item

from  dateutil.parser import parse as fromisoformat


MONTHS = {
        'ஜனவரி' : 'Jan'
        ,'பிப்ரவரி': 'Feb'
        ,'மார்ச்': 'Mar'
        ,'ஏப்ரல்' : 'Apr'
        ,'மே' : 'May'
        ,'ஜூன்' : 'Jun'
        ,'ஜூலை': 'Jul'
        ,'ஆகஸ்ட்': 'Aug'
        ,'செப்டம்பர்': 'Sep'
        ,'அக்டோபர்': 'Oct'
        ,'நவம்பர்': 'Nov'
        ,'டிசம்பர்': 'Dec'
}

class dinamalarSpider(CrawlSpider):
    name = 'dinamalar_spider'
    allowed_domains = ['dinamalar.com']
    start_urls = ['http://www.dinamalar.com']


    rules = [
        
        Rule(
            LinkExtractor(
                allow=[r'.*'],

            ),
            callback='parse_news',
            follow=True,
        ),
    ]


    errored_count = 0

    def _make_date(self, date_string):
        print('date: ', date_string)
        for k, v in MONTHS.items():
            date_string = date_string.replace(k, v)

        date_string = date_string.split(':')[-1]
        print('date: ', date_string)
        return fromisoformat(date_string)


    def parse_links(self, response):
        self.logger.info('firing requests')
        links = [
	    urllib.parse.unquote(i)  for i in response.xpath(
	        '//*[@href][not(contains(@href,"javascript") or contains(@href,"mailto"))]/@href'
	    ).extract()
        ]

        for link in links:
            link = response.urljoin(link)
            self.logger.debug('requesting {}'.format(link))
            yield scrapy.Request(url=link)
        
    def parse_news(self, response):

        if self.errored_count and self.errored_count % 20 == 0:
            print('errored_count:{}'.format(self.errored_count))
            pprint(self.crawler.stats.get_stats())

        try:
            selector     = response.xpath(
                '//div[@id="matter" and @class="newsdet"]'
            )
            		
		
            if not selector:
                self.logger.debug('not a page of interest...')
                return
            
            item = Item()

            item['url']        = response.url                                                      
            item['filename']   = response.url.split('/')[-1].split('?')[0]                         
            item['breadcrumb'] = response.xpath(
                '//div[@id="box_title"]/h3/a/text()'
            ).extract()
            
            author = selector.xpath(
                './/span[contains(@class,"contributor-name")]/text()'
            )

            
            if author:
                item['author'] = [i.extract().strip() for i in author]
            else:
                item['author'] = []
            
            item['date']    = ' '.join(selector.xpath(
                './/div[contains(@class,"mvp-author-info-date")]/text()'
            ).extract()).strip()

            item['date']    =  self._make_date(item['date'])

            item['content'] = selector.xpath(
                './/div[contains(@id, "mvp-content-main")]'
            ).extract()
            
            item['content'] = '\n\n'.join([
                remove_tags(remove_tags_with_content(content, ('script', ))).strip()
                for content in item['content']
            ]).strip()
            
            item['title']   = selector.xpath(
                './/div[@class="newsdetbd1"]/h1/text()'
            )[0].extract().strip()
            
            item['tags']    = selector.xpath(
                './/div[contains(@class, "tags")]/span/a/text()'
            ).extract()

            pprint(item)
            
            yield item

        except KeyboardInterrupt:
            print('got killed by the keyboard :(')
            raise KeyboardInterrupt
        except:
            self.errored_count += 1
            self.logger.exception(urllib.parse.unquote(response.url))
            
