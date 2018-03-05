# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_scrapy.items import News
from urllib.parse import urljoin
from scrapy_redis.spiders import RedisCrawlSpider

class IfengNewsSpider(RedisCrawlSpider):
	name = 'ifeng_news'
	allowed_domains = ['ifeng.com']

	rules=(Rule(LinkExtractor(allow=('[0-9]+\.shtml'),deny=('house'),
		restrict_xpaths=('//a')),
	callback="parse_item",follow=True),
	Rule(LinkExtractor(allow=('list\.shtml'),
		restrict_xpaths=('//ul[contains(@class,"clearfix")]')),follow=True),
	)

	def parse_item(self,response):
		news=News()
		title=response.xpath('//h1[contains(@id,"artical_topic")]/text()')
		if title is None or len(title)==0:
			return
		news["title"]=title[0].extract().encode('utf-8')

		pics=response.xpath('//p[contains(@class,"detailPic")]/img/@src')
		if pics is not None and len(pics)>0:
			news["picture"]=''.join(pics.extract());
			pictureInfo=response.xpath('//p[contains(@class,"picIntro")]/text()')
			if pictureInfo is not None:
				news["picture_info"]=''.join(pics.extract()).encode('utf-8')
			else:
				news["picture_info"]="Null"
		else:
			news["picture"]="Null"
			news["picture_info"]="Null"

		content=response.xpath('//div[contains(@id,"main_content")]/p/text()')
		if content is None or len(content)==0:
			return
		else:
			news["content"]="\n".join(content.extract()).encode('utf-8')

		source=response.xpath('//span[contains(@itemprop,"publisher")]/span/a/text()')
		if source is None or len(source)==0:
			news["source"]="Null"
		else:
			news["source"]=''.join(source.extract()).encode('utf-8')

		time=response.xpath('//span[contains(@itemprop,"datePublished")]/text()')
		if time is None or len(time)==0:
			news["time"]="Null"
		else:
			news["time"]=''.join(time.extract()).encode('utf-8')

		news["url"]=response.url

		newstype=response.xpath('//div[contains(@class,"theLogo")]/div/a/text()')
		if newstype is None or len(newstype)==0:
			news["news_type"]="Null"
		else:
			news["news_type"]=newstype[0].extract().encode('utf-8')

		yield news
