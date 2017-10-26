# -*- coding: utf-8 -*-
import scrapy
from house_spider.items import FangFangItem

import time
from lib.db import DB
from lib.log import Log
import re


class FangFangSpider(scrapy.Spider):
    name = "fang_fang"
    allowed_domains = ["fang.com"]
    start_urls = ['http://newhouse.sz.fang.com/house/s/']
    city_name = '深圳'
    city_id = '85'
    new_house_url = 'http://newhouse.sz.fang.com/'

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 20,
        'COOKIES_ENABLED': False,
        'ITEM_PIPELINES': {
            'house_spider.pipelines.FangFangSpiderPipeline': 300
        }
    }

    def parse(self, response):
        print('1111111111111111')
        # sql = 'select * from fang_city limit 617,50'
        sql = 'select * from fang_city where name not in(select city_name from fang_fang group by city_name) limit 1,1'
        data = DB.connect().fetch_all(sql)

        if not data:
            self.log('"%s"没有需要抓取的数据')
            Log.info('[crawling] "%s"没有需要抓取的数据')

        for row in data:
            self.city_name = row['name']
            self.city_id = row['id']
            self.new_house_url = row['new_house_url']
            # req = self.make_requests_from_url(row['new_house_url'])
            url = row['new_house_url'].strip()
            yield scrapy.Request(url, callback=self.parse_url,
                                 meta={'city_id': row['id'], 'new_house_url': row['new_house_url'],
                                       'city_name': row['name']})

    def parse_url(self, response):
        meta = response.meta
        print(meta)
        # 取页码
        # total_page_tmp = response.xpath('//div[@class="otherpage"]/span[last()]/text()').extract_first()
        # 默认页码为1，兼容房源只有一页的城市报错
        total_page = 1
        total_page_tmp = response.xpath('//li[@class="fr"]/a[@class="last"]/@href').extract_first()
        if total_page_tmp:
            # total_page = total_page_tmp.encode('gbk', 'ignore').decode('utf-8').lstrip('/')
            total_page = re.search(r'/house/s/b9(.*)/', total_page_tmp).group(1)
        else:
            total_page_tmp_list = response.xpath('//ul[@class="page"]/li[@class="pagenum"]/a[@class="snall"]')
            for page_tmp in total_page_tmp_list:
                if page_tmp.xpath('text()').extract_first() == '尾页':
                    total_page = page_tmp.xpath('@href').extract_first().lstrip('/house/s/b9').rstrip('/')
        max_total_page = int(total_page) + 1

        for i in range(1, max_total_page):
            # 有些城市没有后面的斜线，这里要统一处理，坑-。-
            request_url = response.meta['new_house_url'].rstrip('/') + "/house/s/b9" + str(i)
            yield scrapy.Request(request_url, callback=self.parse_list, meta=meta)

    def parse_list(self, response):
        meta = response.meta
        url_list = response.css('div[class="nlcd_name"] a::attr(href)').extract()
        if not url_list:
            url_list = response.css(
                'div[class="sslalone"] ul[class="sslainfor"] li:nth-child(1) strong a::attr(href)').extract()
        for url_single in url_list:
            yield scrapy.Request(url_single.rstrip('/'), callback=self.parse_detail_url, meta=meta)

    def parse_detail_url(self, response):
        meta = response.meta
        detail_url = response.css('div[class="fl more"] p a::attr(href)').extract_first()
        if not detail_url:
            detail_url = response.css('div[class="fn-line"] a::attr(href)').extract_first()

        # if not detail_url:
        #     with open("1.html",'a') as f:
        #         f.write(response.url)
        yield scrapy.Request(detail_url, callback=self.parse_detail, meta=meta)

    def parse_detail(self, response):

        item = FangFangItem()
        item['arg_price'] = response.xpath('//div[@class="main-info-price"]/em/text()').extract_first()
        item['user_rate'] = response.xpath('//div[@class="main-info-comment"]/a/span[2]/text()').extract_first()
        item['name'] = response.xpath('//div[@class="lpbt tf jq_nav"]/h1/a/text()').extract_first()
        item['alias_name'] = response.xpath('//div[@class="lpbt tf jq_nav"]/span/text()').extract_first()
        if item['alias_name']:
            item['alias_name'] = item['alias_name'].lstrip('别名：')
        item['url'] = response.url

        item_list = response.xpath('//ul[@class="list clearfix"]/li')

        # 建筑类别
        item['construct_type'] = response.css(
            '.main-item ul li:nth-child(3) div[class="list-right"] span::text').extract_first()
        # 装修状况
        item['decoration_status'] = response.css(
            '.main-item ul li:nth-child(4) div[class="list-right"]::text').extract_first()
        # 产权年限
        item['right_years'] = response.css(
            '.main-item ul li:nth-child(5) div[class="list-right"] p::text').extract_first()
        # 环线位置
        item['loop_position'] = response.css(
            '.main-item ul li:nth-child(6) div[class="list-right"]::text').extract_first()
        # 开发商
        item['developers'] = response.css(
            '.main-item ul li:nth-child(7) div[class="list-right-text"] a::text').extract_first()
        # 楼盘地址
        item['build_address'] = response.css(
            '.main-item ul li:nth-child(3) div[class="list-right"]::text').extract_first()

        for item_single in item_list:
            item_content = item_single.xpath('div[@class="list-left"]/text()').extract_first()
            # print(item_content)

            if item_content == '物业类别：':
                item['property'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if item_content == '项目特色：':
                project_feature_xpath = item_single.xpath('div[@class="list-right"]/span')
                project_feature_list = ''
                for single_feature in project_feature_xpath:
                    project_feature_list = project_feature_list + single_feature.xpath('text()').extract_first() + ','

                item['project_feature'] = project_feature_list

            if item_content == '销售状态：':
                item['sale_status'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if item_content == '楼盘优惠：':
                item['property_concessions'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if item_content == '开盘时间：':
                item['open_time'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if item_content == '交房时间：':
                item['delivery_time'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if item_content == '售楼地址：':
                item['sale_address'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if item_content == '咨询电话：':
                item['hotline'] = item_single.xpath('div[@class="list-right c00"]/text()').extract_first()
                if not item['hotline']:
                    item['hotline'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if item_content == '主力户型：':
                item['main_unit_type'] = item_single.xpath('div[@class="list-right-text"]/a/text()').extract_first()

        area_list = response.xpath('//ul[@class="clearfix list"]/li')
        for item_single in area_list:
            area_content = item_single.xpath('div[@class="list-left"]/text()').extract_first()
            # print(area_content)
            if area_content == '占地面积：':
                item['area'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if area_content == '建筑面积：':
                item['construct_area'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if area_content == '容':
                item['volume_rate'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if area_content == '绿':
                item['green_rate'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if area_content == '停':
                item['park_space'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if area_content == '停车位配置：':
                item['park_space'] = item_single.xpath('div[@class="list-right-floor"]/text()').extract_first()

            if area_content == '楼栋总数：':
                item['total_build'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if area_content == '总':
                item['total_house'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if area_content == '物业公司：':
                item['property_company'] = item_single.xpath('div[@class="list-right"]/a/text()').extract_first()

            if area_content == '物' or area_content == '物业费：':
                item['property_costs'] = item_single.xpath('div[@class="list-right"]/text()').extract_first()

            if area_content == '楼层状况：' or area_content == '楼层说明：':
                item['floor_condition'] = item_single.xpath('div[@class="list-right-floor"]/text()').extract_first()

        item['traffic_condition'] = response.xpath('//div[@class="set "]/p/text()').extract_first()
        if not item['traffic_condition']:
            item['traffic_condition'] = response.xpath('//div[@class="set "]/text()').extract_first()
        item['project_support'] = response.xpath('//div[@class="set bd-1"]/p/text()').extract_first()
        item['project_desc'] = response.xpath('//div[@class="main-item"]/p[@class="intro"]/text()').extract_first()
        item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        res_item = {}
        for k, v in item.items():
            if v is None:
                res_item[k] = ''
            else:
                res_item[k] = v.strip().replace("\n", "").replace("\r", "").replace('\xa0', '').replace("\r\n", "")

        res_item['city_name'] = response.meta['city_name']
        res_item['city_id'] = response.meta['city_id']
        house_type_url_list = response.url.split('/')
        res_item['house_type_url_id'] = house_type_url_list[len(house_type_url_list) - 2]

        yield res_item
