
articles   = response.xpath('//section[contains(@class, "pt-main-news-section")]')
for article in artciles:
    item = Item()
    item['url']        = response.url                                                      
    .
    .
    .
    author_date = artcile.xpath('//div[@class=article-author]')
    item['author'] = author_date.xpath('//a/text()').extract()
        

    item['date']    = selector.xpath(
        '//span[contains(@class,"pull-right")]/text()'
    ).extract()[0].strip()
