# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChchchItem(scrapy.Item):
    title    = scrapy.Field()
    author   = scrapy.Field()
    content  = scrapy.Field()
    date     = scrapy.Field()
    filename = scrapy.Field()
    url      = scrapy.Field()
    tags = scrapy.Field()
    breadcrumb = scrapy.Field()

class HindutamilItem(ChchchItem):
    pass
