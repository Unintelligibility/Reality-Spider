# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_scrapy.items import News
from urlparse import urljoin

class NewsSpider(CrawlSpider):
	name = 'news'
	allowed_domains = ['sina.com.cn']
	start_urls = [
	'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_1.shtml',#国内 内地
	'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_2.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_3.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_4.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_5.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/gatxw/index_1.shtml',#港台
	'http://roll.news.sina.com.cn/news/gnxw/gatxw/index_2.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/gatxw/index_3.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/gatxw/index_4.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/gatxw/index_5.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/zs-pl/index_1.shtml',#综述
	'http://roll.news.sina.com.cn/news/gnxw/zs-pl/index_2.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/zs-pl/index_3.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/zs-pl/index_4.shtml',
	'http://roll.news.sina.com.cn/news/gnxw/zs-pl/index_5.shtml',
	'http://roll.news.sina.com.cn/news/gjxw/gjmtjj/index_1.shtml',#环球视野
	'http://roll.news.sina.com.cn/news/gjxw/gjmtjj/index_2.shtml',
	'http://roll.news.sina.com.cn/news/gjxw/gjmtjj/index_3.shtml',
	'http://roll.news.sina.com.cn/news/gjxw/gjmtjj/index_4.shtml',
	'http://roll.news.sina.com.cn/news/gjxw/gjmtjj/index_5.shtml',
	'http://roll.news.sina.com.cn/news/gjxw/hqqw/index_1.shtml',#环球趣闻
	'http://roll.news.sina.com.cn/news/gjxw/hqqw/index_2.shtml',
	'http://roll.news.sina.com.cn/news/gjxw/hqqw/index_3.shtml',
	'http://roll.news.sina.com.cn/news/gjxw/hqqw/index_4.shtml',
	'http://roll.news.sina.com.cn/news/gjxw/hqqw/index_5.shtml',
	'http://roll.news.sina.com.cn/news/shxw/zqsk/index_1.shtml',#真情时刻
	'http://roll.news.sina.com.cn/news/shxw/zqsk/index_2.shtml',
	'http://roll.news.sina.com.cn/news/shxw/zqsk/index_3.shtml',
	'http://roll.news.sina.com.cn/news/shxw/zqsk/index_4.shtml',
	'http://roll.news.sina.com.cn/news/shxw/zqsk/index_5.shtml',
	'http://roll.news.sina.com.cn/news/shxw/fz-shyf/index.shtml',#社会与法
	'http://roll.news.sina.com.cn/news/shxw/fz-shyf/index_2.shtml',
	'http://roll.news.sina.com.cn/news/shxw/fz-shyf/index_3.shtml',
	'http://roll.news.sina.com.cn/news/shxw/fz-shyf/index_4.shtml',
	'http://roll.news.sina.com.cn/news/shxw/fz-shyf/index_5.shtml',
	'http://roll.news.sina.com.cn/news/shxw/qwys/index.shtml',#奇闻逸事
	'http://roll.news.sina.com.cn/news/shxw/qwys/index_2.shtml',
	'http://roll.news.sina.com.cn/news/shxw/qwys/index_3.shtml',
	'http://roll.news.sina.com.cn/news/shxw/qwys/index_4.shtml',
	'http://roll.news.sina.com.cn/news/shxw/qwys/index_5.shtml',
	'http://roll.news.sina.com.cn/news/shxw/shwx/index.shtml',#社会万象
	'http://roll.news.sina.com.cn/news/shxw/shwx/index_2.shtml',
	'http://roll.news.sina.com.cn/news/shxw/shwx/index_3.shtml',
	'http://roll.news.sina.com.cn/news/shxw/shwx/index_4.shtml',
	'http://roll.news.sina.com.cn/news/shxw/shwx/index_5.shtml'
	'http://sports.sina.com.cn',
	'http://ent.sina.com.cn',
	]

	rules=(Rule(LinkExtractor(allow=('[0-9]+\.shtml'),#deny=(''),
		restrict_xpaths=('//a')),
	callback="parse_item",follow=True),)

	def parse_item(self,response):
		news=News()
		#新闻标题
		title=response.xpath('//h1/text()')
		# if(title == None):
			# return
		news["title"]=title[0].extract().encode('utf-8')
		news['url']=response.url
		types=response.xpath('//div[contains(@class,"channel-path")]/a/text()')
		if types==None:
			types=response.xpath('//div[contains(@class,"bread")]/a/text()')
		if types!=None:
			news['news_type']=types[0].extract().encode('utf-8')
		else:
			news['news_type']="null"
		#图片url 用反斜号分隔
		picture=response.xpath('//div[contains(@class,"img_wrapper")]/img/@src').extract()
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
