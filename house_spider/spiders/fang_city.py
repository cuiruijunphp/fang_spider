# -*- coding: utf-8 -*-
import scrapy

from house_spider.items import FangCityItem
import time


class FangCitySpider(scrapy.Spider):
    name = "fang_city"
    allowed_domains = ["www.fang.com"]
    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 20,
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES': {
            'house_spider.pipelines.FangCitySpiderPipeline': 300
        }
    }

    def parse(self, response):
        for row in response.xpath('//div[@class="outCont"]/table/tr/td[last()]/a'):
            item = FangCityItem()
            item['url'] = row.xpath('@href').extract_first()
            item['new_house_url'] = item['url'].replace("http://",'http://newhouse.')
            item['second_hand_url'] = item['url'].replace("http://",'http://esf.')
            item['name'] = row.xpath('text()').extract_first()
            item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            item['province'] = row.xpath('../../td[2]/strong/text()').extract_first()
            if item['province']:
                item['province'] = item['province'].strip('\xa0')
            if not item['province']:
                id_name = row.xpath('../../@id').extract_first()
                item['province'] = row.xpath('../../preceding-sibling::tr[@id="'+id_name+'"][last()]/td[2]/strong/text()').extract_first()
            yield item
