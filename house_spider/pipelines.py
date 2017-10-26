# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import math
from scrapy.exceptions import DropItem

from lib.db import DB


class HouseSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class FangCitySpiderPipeline(object):
    @staticmethod
    def process_item(item, spider):
        if item['name']:
            DB.connect().insert('fang_city', item)
            return item
        else:
            raise DropItem('item由于不完整被丢弃')

class FangFangSpiderPipeline(object):
    @staticmethod
    def process_item(item, spider):
        if item['url']:
            DB.connect().insert('fang_fang', item)
            return item
        else:
            raise DropItem('item由于不完整被丢弃')

class FangHouseTypeSpiderPipeline(object):
    @staticmethod
    def process_item(item, spider):
        if item['name']:
            DB.connect().insert('fang_house_type', item)
            return item
        else:
            raise DropItem('item由于不完整被丢弃')

class XiechengSqSpiderPipeline(object):
    @staticmethod
    def process_item(item, spider):
        if item['name'] :
            DB.connect().insert('xiecheng_sq', item)
            return item
        else:
            raise DropItem('item由于不完整被丢弃')

class XiechengCitySpiderPipeline(object):
    @staticmethod
    def process_item(item, spider):
        if item['name'] and item['city_id']:
            DB.connect().insert('xiecheng_city', item)
            return item
        else:
            raise DropItem('item由于不完整被丢弃')

class CleanHouseResSpiderPipeline(object):
    @staticmethod
    def process_item(item, spider):
        if item['name']:
            DB.connect().insert('house_res', item)
            return item
        else:
            raise DropItem('item由于不完整被丢弃')

