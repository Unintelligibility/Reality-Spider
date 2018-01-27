# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_scrapy.items import News
from urlparse import urljoin

class NewsSpider(CrawlSpider):
	name = 'news'
	allowed_domains = ['news.sina.com.cn']
	start_urls = [
	# 'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_1.shtml',
	# 'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_2.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_3.shtml'
	]

	rules=(Rule(LinkExtractor(allow=('\.shtml'),restrict_xpaths=('//ul[contains(@class,"list_009")]/li/a[@href]')),callback="parse_item",follow=False),)

	def parse_item(self,response):
		news=News()
		#新闻标题
		news["title"]=response.xpath('//h1/text()')[0].extract().encode('utf-8')
		#图片url 用反斜号分隔
		picture=response.xpath('//div[contains(@class,"img_wrapper")]/img/@href').extract()
		for each_pic in picture:
			if "http:" not in each_pic:
				each_pic=urljoin("http:",each_pic)
		news["picture"]='\\'.join(picture)
		if news["picture"]==None:
			news["picture"]=' '
		#图片信息 用反斜号分隔
		news["picture_info"]='\\'.join(response.xpath('//div[contains(@class,"img_wrapper")]/span/text()').extract()).encode('utf-8')
		if news["picture_info"]=='':
			news["picture_info"]==' '
		
		news["content"]='\n'.join(response.xpath('//div[contains(@class,"article")]/p/text()').extract()).encode('utf-8')
		#杂志社信息
		source=response.xpath('//a[contains(@class,"source")]/text()')
		if source!=None and len(source)!=0:
			source=source[0].extract().encode('utf-8')
		else:
			source=response.xpath('//span[contains(@class,"source")]/text()')
			if source!=None and len(source)!=0:
				source=source[0].extract().encode('utf-8')
			else:
				source="未知"
		news["source"]=source
		#时间
		news["time"]=response.xpath('//span[contains(@class,"date")]/text()')[0].extract().encode('utf-8')
		yield news
