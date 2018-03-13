# -*- coding: utf-8 -*-
from dianping.items import DianpingItem
from scrapy.conf import settings
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


'''class DianpingPipeline(object):
    def process_item(self, item, spider):
        return item'''

class MongoPipeline(object):

    def process_item(self, item, spider):
        connection = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
        database = connection[settings['MONGODB_DB']]
        if item['cityName'] == 'Shenzhen':
            self.collection = database[settings['MONGODB_SHENZHEN']].insert(dict(item))
        if item['cityName'] == 'Beijing':
            self.collection = database[settings['MONGODB_BEIJING']].insert(dict(item))
        if item['cityName'] == 'Shanghai':
            self.collection = database[settings['MONGODB_SHANGHAI']].insert(dict(item))
        if item['cityName'] == 'Guangzhou':
            self.collection = database[settings['MONGODB_GUANGZHOU']].insert(dict(item))
        if item['cityName'] == 'Chengdu':
            self.collection = database[settings['MONGODB_CHENGDU']].insert(dict(item))
        if item['cityName'] == 'Nanjing':
            self.collection = database[settings['MONGODB_NANJING']].insert(dict(item))
        if item['cityName'] == 'Suzhou':
            self.collection = database[settings['MONGODB_Suzhou']].insert(dict(item))
        if item['cityName'] == 'Hangzhou':
            self.collection = database[settings['MONGODB_HANGZHOU']].insert(dict(item))

        return item

class MongoPipeline_Shenzhen(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DB']
        client = pymongo.MongoClient(host=host,port=port)
        database = client[dbName]
        self.post = database['Shenzhen']
    def process_item(self, item, spider):
        #update方法失效有效去重？
        self.post.update({'commentContent':item['commentContent']},{'$set':dict(item)},True)

        return item

class MongoPipeline_Chengdu(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DB']
        client = pymongo.MongoClient(host=host,port=port)
        database = client[dbName]
        self.post = database['Chengdu']
    def process_item(self, item, spider):
        #update方法失效有效去重？
        self.post.update({'commentContent':item['commentContent']},{'$set':dict(item)},True)

        return item

class MongoPipeline_Hangzhou(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DB']
        client = pymongo.MongoClient(host=host,port=port)
        database = client[dbName]
        self.post = database['Hangzhou']
    def process_item(self, item, spider):
        #update方法失效有效去重？
        self.post.update({'commentContent':item['commentContent']},{'$set':dict(item)},True)

        return item

class MongoPipeline_Guangzhou(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DB']
        client = pymongo.MongoClient(host=host,port=port)
        database = client[dbName]
        self.post = database['Guangzhou']
    def process_item(self, item, spider):
        #update方法失效有效去重？
        self.post.update({'commentContent':item['commentContent']},{'$set':dict(item)},True)

        return item