# -*- coding: utf-8 -*-
from lib.db import DB
import urllib
import urllib.request
from urllib.request import urlopen, quote
import requests
import json

url = 'http://api.map.baidu.com/geocoder/v2/?callback=renderOption&output=json&ak=gYPsXnyBKXlAiSk5Pq4MmnEW7uwymBsD'

sql = 'select a.name,a.sale_address,c.name as city_name,c.province as province  from fang_fang as a left join fang_city as c on a.city_id=c.id limit 2'

data = DB.connect().fetch_all(sql)

for single_data in data:
    address = ''
    if single_data['sale_address'] not in ['暂无资料','待定','暂无信息','项目现场','暂无展厅','暂无','未开放','暂无售楼处']:
        if single_data['province'] == '直辖市':
            address = single_data['sale_address']
        else:
            address = single_data['province'] + single_data['sale_address']

        req_url = url + '&address='+quote(address)
        req = urllib.request.urlopen(req_url)
        res = req.read()
        print(res)
        temp = json.loads(res)
        print(temp)
        # lat=temp['result']['location']['lat']
        # lng=temp['result']['location']['lng']
        # print(lat)
        # print(lng)










