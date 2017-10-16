# -*- coding: utf-8 -*-
import scrapy

from lib.db import DB
from lib.log import Log

import time
import json

from house_spider.items import XiechengCityItem


class XiechengSubCitySpider(scrapy.Spider):
    name = "xiecheng_sub_city"
    allowed_domains = ["ctrip.com"]
    start_urls = ['http://hotels.ctrip.com/Domestic/Tool/AjaxGetHotKeyword.aspx?cityid=299/']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 20,
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES': {
            'house_spider.pipelines.XiechengCitySpiderPipeline': 300
        }
    }

    def parse(self, response):
        sql = 'select * from xiecheng_city limit 0,350'
        data = DB.connect().fetch_all(sql)

        if not data:
            self.log('"%s"没有需要抓取的数据')
            Log.info('[crawling] "%s"没有需要抓取的数据')

        for row in data:
            if row['city_id']:
                print(row)
                # self.city_name = row['name']
                # self.city_id = row['city_id']
                url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxGetHotKeyword.aspx?cityid='+str(row['city_id'])
                print(url)
                yield scrapy.Request(url, callback=self.parse_detail,meta={'city_id':row['city_id'],'city_name':row['name'],'short_name':row['short_name']})

    def parse_detail(self, response):
        print(response.body_as_unicode())
        if response.body_as_unicode():
            pos = response.body_as_unicode().find('cQuery.jsonpResponse.suggestion')

            if pos > -1 :
                res_json = response.body_as_unicode()[pos:].lstrip("cQuery.jsonpResponse.suggestion=")
                result_list = json.loads(res_json)
                item = XiechengCityItem()
                if result_list['subCity']:
                    sub_city_list = result_list['subCity']['data']

                    for res in sub_city_list:
                        item['name'] = response.meta['city_name']
                        item['city_id'] = response.meta['city_id']
                        item['short_name'] = response.meta['short_name']
                        item['type'] = 'sub_city'
                        item['sub_city_name'] = res['name']
                        item['sub_city_short_name'] = res['ename']
                        item['sub_city_id'] = res['id']
                        item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

                        yield item

