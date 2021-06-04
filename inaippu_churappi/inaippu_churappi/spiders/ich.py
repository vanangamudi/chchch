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



import urllib
from w3lib.url import url_query_cleaner
from url_normalize import url_normalize

def clean_url(url):
    url = url_normalize(url)
    url = url_query_cleaner(url,
                            parameterlist = [
                                'utm_source',
                                'utm_medium',
                                'utm_campaign',
                                'utm_term',
                                'utm_content'
                            ],
                            remove=True)

    url = url.replace('//www.', '//')
    
    url = url.replace('http://', '')
    url = url.replace('https://', '')

    if url.endswith("/"):
        url = url[:-1]
    return url

def get_base_url(url):
    url = clean_url(url)
    return url.split('/')[0]

class IchSpider(CrawlSpider):
    name = 'ich'
    rules = [
        
        Rule(
            LinkExtractor(allow=[r'/.*']),
            callback='parse_link',
            follow=True,
        ),
        
    ]

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        
        self.start_urls = kwargs.pop('start_urls').split(',')
        self.allowed_domains = [get_base_url(url) for url in self.start_urls]

        print('start urls: {}'.format(self.start_urls))


    def parse_link(self, response):
        item = Item()
        item['url'] = urllib.parse.unquote(response.url)
        return item
