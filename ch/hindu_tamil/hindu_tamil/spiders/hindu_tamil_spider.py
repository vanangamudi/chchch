import bs4
import pdb
from w3lib.html import remove_tags, remove_tags_with_content

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from hindu_tamil.items import HinduTamilItem

class HinduTamilSpiderSpider(CrawlSpider):
    name = 'hindu_tamil_spider'
    allowed_domains = ['hindutamil.in']
    start_urls = ['http://hindutamil.in/']

    rules = [
        
        Rule(
            LinkExtractor(allow=[r'/.*']),
            callback='parse_news',
            follow=True,
        ),

    ]

        
    def parse_news(self, response):

        selector     = response.xpath('//div[contains(@class, "article-section")]')
        publish_info = selector.xpath('//div[contains(@class,"publish-info")]')
        
        if selector:
            item = HinduTamilItem()

            item['url']        = response.url                                                      
            item['filename']   = response.url.split('/')[-1].split('?')[0]                         
            item['breadcrumb'] = response.xpath('//ol[@class="breadcrumb"]/li/a/text()').extract() 
            

            item['author']  = publish_info.xpath('string(//div[contains(@class,"author-name")])')[0].extract() 
            item['date']    = publish_info.xpath('//span[contains(@class,"date")]/text()')[0].extract()        
            item['content'] = publish_info.xpath('//div[contains(@class, "pgContent")]')[0].extract()
            item['content'] = remove_tags(remove_tags_with_content(item['content'], ('script', )))
            
            item['title']   = selector.xpath('//h1[contains(@class,"art-title")]/text()')[0].extract()
            item['tags']    = selector.xpath('//div[contains(@class, "article-categories")]/a/text()').extract()

            yield item
