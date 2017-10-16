# -*- coding: utf-8 -*-
import scrapy

import gzip
import urllib
from bs4 import BeautifulSoup
from io import StringIO
from lxml import etree
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector


class TestDetailFangSpider(scrapy.Spider):
    name = "test_detail_fang"
    allowed_domains = ["fang.com"]
    start_urls = ['http://gongyuanhuabanli.fang.com//house/2810135162/housedetail.htm']

    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #         'house_spider.middlewares.RandomUserAgentMiddleware': 400,
    #         'scrapy.downloadermiddlewares.retry.RetryMiddleware': 410,
    #     }
    # }
    DOWNLOADER_MIDDLEWARES = {
    'scrapy_beautifulsoup.middleware.BeautifulSoupMiddleware': 543
    }
    BEAUTIFULSOUP_PARSER = "html5lib"

    def start_requests(self):
        # header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate, sdch','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        url = 'http://gongyuanhuabanli.fang.com//house/2810135162/housedetail.htm'
        yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):

        # content = urllib.request.urlopen(response.url).read()
        # content = gzip.decompress(content).decode("gb18030") #网页gb2312的编码要用这个
        # print(content)
        # soup = BeautifulSoup(content, "lxml")

        # jianzu_type = response.xpath('//ul[@class="list clearfix"][1]/li')
        # print(jianzu_type)
        # for item in jianzu_type:
        #     print(item)
        #     print(item.xpath('div[@class="list-left"]/text()'))

        print('111111111111111111')
        print(response.xpath('//div[@class="lpbt tf jq_nav"]/h1/a/text()').extract_first())
        print(response.xpath('//div[@class="main-info-price"]/em/text()').extract_first())


        # content = StringIO.StringIO(response)
        # gzipper = gzip.GzipFile(fileobj=content)
        # content = gzipper.read().decode('gbk')

        # start = response.body_as_unicode().find('建筑类别：')
        # start_ = start - 100
        # end = start + 260
        # print(response.body_as_unicode()[start_:end])

        # print(response.body_as_unicode().find('建筑类别：'))
        # if response.body_as_unicode().find('建筑类别：'):
        aaa = response.xpath('/html/body/div[8]/div/div[1]/div[1]/ul/li[3]/div[1]/text()').extract_first()
        # print(aaa)

    def parse_tmp(self,response):
        soup = BeautifulSoup(response.body, 'html5lib')
        jianzu_type = soup.xpath('//ul[@class="list clearfix"]/li')
        for item in jianzu_type:
            print(item)
            print(item.xpath('div[@class="list-left"]/text()'))


