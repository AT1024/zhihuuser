# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''这是新建项目时自动生成的item pipeline 组件类，你可以改名字，但改完之后要在配置文件的ITEM_PIPELINES修改'''
'''
class ZhihuuserPipeline(object):
    def process_item(self, item, spider):
        return item
'''
import pymongo

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 这也是一种去重手段，第三个参数为True，则会根据前面的查找，查找到了执行更新，  查找不到就添加一个
        self.db['user'].update({'url_token':item['url_token']},{'$set':item},True)
        return item
