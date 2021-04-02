
import bs4
import pdb
from w3lib.html import remove_tags, remove_tags_with_content

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from chchch.items import HindutamilItem

from w3lib.url import url_query_cleaner
from url_normalize import url_normalize

def canonicalize_url(u):
    """
    taken from https://stackoverflow.com/a/59892876/1685729
    """
    
    u = url_normalize(u)
    u = url_query_cleaner(u,parameterlist = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'],remove=True)

    if u.startswith("http://"):
        u = u[7:]
    if u.startswith("https://"):
        u = u[8:]
    if u.startswith("www."):
        u = u[4:]
    if u.endswith("/"):
        u = u[:-1]
    return u
        
class HindutamilSpider(CrawlSpider):
    name = 'hindutamil'
    allowed_domains = ['www.hindutamil.in']
    start_urls = ['http://www.hindutamil.in/']

    rules = [

        Rule(
            LinkExtractor(allow=[r'/.*']),
            callback='parse',
            follow=True,
        ),

    ]
   
    def parse(self, response):
        try:
            selector = response.xpath('//div[contains(@class, "article-section")]')
            if selector:
                item = HindutamilItem()
                
                item['url'] = canonicalize_url(response.url)
                item['filename'] = response.url.split('/')[-1].split('?')[0]
                
                item['breadcrumb'] = response.xpath('//ol[@class="breadcrumb"]/li/a/text()').extract()
                
                publish_info = selector.xpath('//div[contains(@class,"publish-info")]')
                item['author'] = publish_info.xpath('string(//div[contains(@class,"author-name")])')[0].extract()
                item['date']   = publish_info.xpath('//span[contains(@class,"date")]/text()')[0].extract()
                
                item['title'] = selector.xpath('//h1[contains(@class,"art-title")]/text()')[0].extract()
                
                item['content'] = publish_info.xpath('//div[contains(@class, "pgContent")]')[0].extract()
                item['content'] = remove_tags(remove_tags_with_content(item['content'], ('script', )))
                
                item['tags'] = selector.xpath('//div[contains(@class, "article-categories")]/a/text()').extract()
                
            yield item
        except:
            print('*** errored *** {}'.format(response.url))
