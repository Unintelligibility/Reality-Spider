# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class News(scrapy.Item):
    title = scrapy.Field()
    picture=scrapy.Field()
    picture_info=scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    news_type = scrapy.Field()
    pass
