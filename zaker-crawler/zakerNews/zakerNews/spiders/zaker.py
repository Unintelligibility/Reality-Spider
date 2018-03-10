# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zakerNews.items import News
import re
import datetime

class ZakerCrawlSpider(CrawlSpider):
    name = 'zaker'
    allowed_domains = ['myzaker.com']
    start_urls = ['https://www.myzaker.com/channel/660','https://www.myzaker.com/channel/9']

    rules=(Rule(LinkExtractor(allow=('//www.myzaker.com/article/[a-z0-9]+/$'),
		restrict_xpaths=('//a')),
	callback="parse_item",follow=False),)

    def parse_item(self, response):
    	news = News()
    	title = response.xpath('//h1')[0].extract()
    	img = response.xpath('//div[contains(@id,"id_imagebox_0")]/div/img/@data-original')[0].extract()
    	source = response.xpath('//span[contains(@class,"auther")]/text()')[0].extract()
    	time = response.xpath('//span[contains(@class,"time")]/text()')[0].extract()

    	content_text = response.xpath('//h1/text()')[0].extract()+'.'.join(response.xpath('//div[contains(@class,"article_content")]//text()').extract())
    	header_html = response.xpath('//div[contains(@class,"article_header")]')[0].extract()
    	#正则不对
    	header_html = re.sub(r'<span class="time">[0-9]*小时前</span>',"<span class='time'>"+time.strftime("%Y-%m-%d", time.localtime())+"</span>",header_html)
    	header_html = re.sub(r'<span class="time">昨天</span>','<span class="time">'+getDayBefore(daynum=1)+'</span>',header_html)
    	header_html = re.sub(r'<span class="time">前天</span>',getDayBefore(daynum=2),header_html)

    	content_html = header_html + response.xpath('//div[contains(@id,"content")]')[1].extract()
    	content_html = content_html.replace('data-original','src')

    	news_type = response.xpath('//ol[contains(@class,"breadcrumb")]/li//text()')[1].extract()
		news_tags = ';'.join(response.xpath('//div[contains(@class,"article_more")]/a//text()').extract())
    	
    	self.logger.info(title)
        pass

    def getDayBefore(self,daynum):
    	today=datetime.date.today() 
		days=datetime.timedelta(days=daynum) 
    	thatDay=today-days
    	return thatDay