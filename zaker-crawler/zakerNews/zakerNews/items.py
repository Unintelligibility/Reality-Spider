# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class News(scrapy.Item):
	#标题
    title = scrapy.Field()
    #缩略图
    picture=scrapy.Field()
    #媒体
    source = scrapy.Field()
    #时间
    time = scrapy.Field()
    #文本内容
    content_text = scrapy.Field()
    #html内容
    content_html = scrapy.Field()
    #分类
    news_type = scrapy.Field()
    #标签
    news_tags = scrapy.Field()
    pass
