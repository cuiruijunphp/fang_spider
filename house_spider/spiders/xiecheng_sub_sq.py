# -*- coding: utf-8 -*-
import scrapy
import json

import time

from house_spider.items import XiechengSqItem

from lib.db import DB
from lib.log import Log


class XiechengSubSqSpider(scrapy.Spider):
    name = "xiecheng_sub_sq"
    allowed_domains = ["ctrip.com"]
    start_urls = ['http://hotels.ctrip.com/domestic/tool/AjaxCityZoneNew.aspx?city=30']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 20,
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES': {
            'house_spider.pipelines.XiechengSqSpiderPipeline': 300
        }
    }

    def parse(self, response):
        sql = 'select * from xiecheng_city limit 350,1650'
        data = DB.connect().fetch_all(sql)

        if not data:
            self.log('"%s"没有需要抓取的数据')
            Log.info('[crawling] "%s"没有需要抓取的数据')

        for row in data:
            if row['city_id']:
                self.city_name = row['name']
                self.city_id = row['city_id']
                url = 'http://hotels.ctrip.com/domestic/tool/AjaxCityZoneNew.aspx?city=' + str(row['sub_city_id'])
                yield scrapy.Request(url, callback=self.parse_detail,
                                     meta={'city_id': row['city_id'], 'city_name': row['name'],
                                           'sub_city_name': row['sub_city_name']})

    def parse_detail(self, response):

        if response.body_as_unicode():
            res_json = response.body_as_unicode().lstrip('cQuery.jsonpResponse').strip(' ').lstrip('=').strip(' ')

            result_list = json.loads(res_json)
            print(result_list)
            item = XiechengSqItem()

            keys_temp = ','.join(result_list.keys())
            res_keys = keys_temp.split(',')
            print('11111111111111')
            print(res_keys)
            res_list = []
            for i in range(len(res_keys)):
                res_list += result_list[res_keys[i]]
            # res_list = result_list['ABCDE'] + result_list['FGHJK'] + result_list['LMNOP'] + result_list['QRSTW'] + result_list['XYZ']
            print(res_list)

            for res in res_list:
                item['name'] = res['name']
                item['desc'] = res['desc']
                item['lat'] = res['lat']
                item['lng'] = res['lng']
                # item['path'] = json.JSONEncoder().encode(res['path'])
                item['path'] = json.JSONEncoder().encode(res['path'])
                item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                item['city_name'] = response.meta['city_name']
                item['city_id'] = response.meta['city_id']
                item['sub_city_name'] = response.meta['sub_city_name']

                yield item
