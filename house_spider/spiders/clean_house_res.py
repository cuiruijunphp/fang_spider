# -*- coding: utf-8 -*-
import scrapy
from lib.db import DB
from urllib.request import quote
import json
from house_spider.items import CleanHouseResItem
import time

class CleanHouseResSpider(scrapy.Spider):
    name = "clean_house_res"
    allowed_domains = ["baidu.com"]
    start_urls = ['http://api.map.baidu.com/geocoder/v2']
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 20,
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES': {
            'house_spider.pipelines.CleanHouseResSpiderPipeline': 300
        }
    }

    def parse(self, response):
        url = 'http://api.map.baidu.com/geocoder/v2/?callback=renderOption&output=json&ak=gYPsXnyBKXlAiSk5Pq4MmnEW7uwymBsD'

        sql = 'select a.name,a.sale_address,a.project_desc as proj_desc,c.name as city_name,c.province as province  from fang_fang as a left join fang_city as c on a.city_id=c.id limit 2'

        data = DB.connect().fetch_all(sql)

        for single_data in data:
            address = ''
            if single_data['sale_address'] not in ['暂无资料','待定','暂无信息','项目现场','暂无展厅','暂无','未开放','暂无售楼处']:
                if single_data['province'] == '直辖市':
                    address = single_data['sale_address']
                else:
                    address = single_data['province'] + single_data['sale_address']

                req_url = url + '&address='+quote(address)
                yield  scrapy.Request(req_url, callback=self.parse_url,
                                 meta={'name': single_data['name'], 'address': single_data['sale_address'],
                                       'city_name': single_data['city_name'],'proj_desc': single_data['proj_desc']})

    def parse_url(self,response):
        json_str = response.body_as_unicode().lstrip('renderOption&&renderOption').lstrip('(').rstrip(')')
        res_json = json.loads(json_str)
        if res_json['status'] == 0:
            item = CleanHouseResItem()
            item['lat'] = str(res_json['result']['location']['lat'])
            item['lng'] = str(res_json['result']['location']['lng'])
            item['name'] = response.meta['name']
            item['address'] = response.meta['address']
            item['name'] = response.meta['name']
            item['city_name'] = response.meta['city_name']
            item['proj_desc'] = response.meta['proj_desc']
            item['is_second_house'] = 0
            item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            yield item
