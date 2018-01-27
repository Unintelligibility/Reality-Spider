# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class MongoPipeline(object):

	def __init__(self,mongo_uri,mongo_port,mongo_db,mongo_coll):
		self.uri=mongo_uri
		self.port=mongo_port
		self.mongo_db=mongo_db
		self.coll=mongo_coll

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri=crawler.settings.get('MONGO_URL'),
			mongo_port=crawler.settings.get('MONGO_PORT'),
			mongo_db=crawler.settings.get('MONGO_DB'),
			mongo_coll=crawler.settings.get('MONGO_COLL')
		)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(host=self.uri,port=self.port)
		self.db = self.client[self.mongo_db]

	def close_spider(self,spider):
		self.client.close()

	def process_item(self, item, spider):
		postItem = dict(item)  # 把item转化成字典形式
		self.db[self.coll].insert(postItem)  # 向数据库插入一条记录
		# return item  # 会在控制台输出原item数据，可以选择不写
