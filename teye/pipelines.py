# -*- coding: utf-8 -*-

from pymongo import MongoClient
import pprint

class TYCPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["eye"]

    def process_item(self, item, spider):
        if spider.name == "eye":
            self.collection.insert(item)
            print("保存成功")

        return item


class DPingPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["dping"]

    def process_item(self, item, spider):
        if spider.name == "dping":
            self.collection.insert(item)
            print("保存成功")
            # pprint.pprint(item)
        return item























