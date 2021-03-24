import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from chchch.items import HindutamilItem

import bs4

import pdb

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

    """
    def parse_listing(self, response):
        links = response.xpath('//a[not(contains(@href, "javascript:"))]/@href').extract()
        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url)
    """
    def parse(self, response):
        #self.parse_listing(response)

        selector = response.xpath('//div[contains(@class, "article-section")]')
        if selector:
            item = HindutamilItem()

            item['url'] = response.url
            item['filename'] = response.url.split('/')[-1].split('?')[0]

            item['breadcrumb'] = response.xpath('//ol[@class="breadcrumb"]/li/a/text()').extract()

            publish_info = selector.xpath('//div[contains(@class,"publish-info")]')
            item['author'] = publish_info.xpath('string(//div[contains(@class,"author-name")])')[0].extract()
            item['date']   = publish_info.xpath('//span[contains(@class,"date")]/text()')[0].extract()
           
            item['title'] = selector.xpath('//h1[contains(@class,"art-title")]/text()')[0].extract()

            item['content'] = selector.xpath('//div[contains(@class, "pgContent")]//p//text()').extract()
            item['content'] = '\n\n'.join(item['content']).replace('\r\n', '\n')


            item['tags'] = selector.xpath('//div[contains(@class, "article-categories")]/a/text()').extract()

            yield item
