# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zakerNews.items import News
import re
import datetime
from scrapy_redis.spiders import RedisCrawlSpider


def getDayBefore(daynum):
    today=datetime.date.today() 
    days=datetime.timedelta(days=daynum) 
    thatDay=today-days
    return thatDay

class ZakerCrawlSpider(RedisCrawlSpider):
    name = 'zaker'
    allowed_domains = ['myzaker.com']
    # start_urls = ['https://www.myzaker.com/channel/660',#热点
    # 'https://www.myzaker.com/channel/1',#国内
    # 'https://www.myzaker.com/channel/2',#国际
    # 'https://www.myzaker.com/channel/3',#军事
    # 'https://www.myzaker.com/channel/4',#财经
    # 'https://www.myzaker.com/channel/5',#互联网
    # 'https://www.myzaker.com/channel/6',#首页？
    # 'https://www.myzaker.com/channel/7',#汽车
    # 'https://www.myzaker.com/channel/8',#体育
    # 'https://www.myzaker.com/channel/9',#娱乐
    # 'https://www.myzaker.com/channel/11',#教育
    # 'https://www.myzaker.com/channel/12',#时尚
    # 'https://www.myzaker.com/channel/13',#科技
    # 'https://www.myzaker.com/channel/14',#社会
    # 'https://www.myzaker.com/channel/959',#亲子
    # 'https://www.myzaker.com/channel/981',#旅游
    # 'https://www.myzaker.com/channel/1039',#科学
    # 'https://www.myzaker.com/channel/1014',#星座
    # 'https://www.myzaker.com/channel/1067',#奢侈品
    # 'https://www.myzaker.com/channel/10376',#游戏
    # 'https://www.myzaker.com/channel/10386',#美食
    # 'https://www.myzaker.com/channel/10530',#电影
    # 'https://www.myzaker.com/channel/10802',#健康
    # 'https://www.myzaker.com/channel/11195'#理财
    # ]

    rules=(Rule(LinkExtractor(allow=('//www.myzaker.com/article/[a-z0-9]+/$'),
		restrict_xpaths=('//a')),
	callback="parse_item",follow=False),)

    def parse_item(self, response):
        news = News()
        title = response.xpath('//h1/text()')[0].extract()
        pic_part=response.xpath('//div[contains(@id,"id_imagebox_0")]/div/img/@data-original')
        if(len(pic_part) is 0):
            return
        picture = pic_part[0].extract()
        source = response.xpath('//span[contains(@class,"auther")]/text()')[0].extract()
        time = response.xpath('//span[contains(@class,"time")]/text()')[0].extract()
        time = re.sub(r'刚刚',str(getDayBefore(daynum=0)),time)
        time = re.sub(r'[0-9]*分钟前',str(getDayBefore(daynum=0)),time)
        time = re.sub(r'[0-9]*小时前',str(getDayBefore(daynum=0)),time)
        time = re.sub(r'昨天',str(getDayBefore(daynum=1)),time)
        time = re.sub(r'前天',str(getDayBefore(daynum=2)),time)

        content_text = (response.xpath('//h1/text()')[0].extract()+'.'.join(response.xpath('//div[contains(@class,"article_content")]//text()').extract()))
        
        header_html = response.xpath('//div[contains(@class,"article_header")]')[0].extract()
        header_html = re.sub(r'刚刚',str(getDayBefore(daynum=0)),header_html)
        header_html = re.sub(r'<span class="time">[0-9]*分钟前</span>','<span class="time">'+str(getDayBefore(daynum=0))+'</span>',header_html)
        header_html = re.sub(r'<span class="time">[0-9]*小时前</span>','<span class="time">'+str(getDayBefore(daynum=0))+'</span>',header_html)
        header_html = re.sub(r'<span class="time">昨天</span>','<span class="time">'+str(getDayBefore(daynum=1))+'</span>',header_html)
        header_html = re.sub(r'<span class="time">前天</span>','<span class="time">'+str(getDayBefore(daynum=2))+'</span>',header_html)

        content_html = response.xpath('//div[contains(@class,"article_content")]')[0].extract().replace('data-original','src')
        content_html = header_html+content_html;

        news_type = response.xpath('//ol[contains(@class,"breadcrumb")]/li//text()')[-2].extract()
        news_tags = (';'.join(response.xpath('//div[contains(@class,"article_more")]/a//text()').extract()))
    
        news["title"]=title
        news["url"]=response.url
        news["picture"]=picture
        news["source"]=source
        news["time"]=time
        news["content_text"]=content_text
        news["content"]=content_html
        news["news_type"]=news_type
        news["news_tags"]=news_tags
        yield news