# -*- coding: utf-8 -*-
import scrapy
import json
from house_spider.items import XiechengCityItem


class XiechengCitySpider(scrapy.Spider):
    name = "xiecheng_city"
    allowed_domains = ["ctrip.com"]
    start_urls = ['http://hotels.ctrip.com/Domestic/Tool/AjaxGetCitySuggestion.aspx']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 20,
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES': {
            'house_spider.pipelines.XiechengCitySpiderPipeline': 300
        }
    }

    def parse(self, response):
        res_json = response.body_as_unicode()
        pos = res_json.find('cQuery.jsonpResponse.suggestion')
        if pos > -1:
            res_json = res_json[pos:].lstrip("cQuery.jsonpResponse.suggestion=")
            # res_json = res_json.replace("'",'\"')
            # print(res_json)
            res_json_1 = res_json.replace("热门", '\"热门\"').replace("ABCD", '\"ABCD\"').replace("EFGH",
                                                                                              '\"EFGH\"').replace(
                "JKLM", '\"JKLM\"').replace("NOPQRS", '\"NOPQRS\"').replace("TUVWX", '\"TUVWX\"').replace("YZ",
                                                                                                          '\"YZ\"').replace(
                "display", '\"display\"').replace("data", '\"data\"').replace("group", '\"group\"').replace("\n",
                                                                                                            "").replace(
                "\r", "").replace('\r\n', '').replace(' ', '').replace('\t', '')
            # res_json = res_json.replace("ABCD",'\"ABCD\"')
            # res_json = res_json.replace("display",'\"display\"')
            # res_json = res_json.replace("data",'\"data\"')
            # res_json = res_json.replace("group",'\"group\"')
            print(res_json_1)
            with open('1.html', 'a+') as f:
                f.write(res_json_1)

        result_list = json.loads(res_json_1)
        print(result_list)
        city_list = result_list['ABCD'] + result_list['EFGH'] + result_list['JKLM'] + result_list['NOPQRS'] + \
                    result_list['TUVWX'] + result_list['YZ']
        item = XiechengCityItem()

        for single_city in city_list:
            single_city_tmp = single_city['data'].split('|')
            item['short_name'] = single_city_tmp[0]
            item['name'] = single_city_tmp[1]
            item['city_id'] = single_city_tmp[2]
            item['type'] = 'city'

            yield item
