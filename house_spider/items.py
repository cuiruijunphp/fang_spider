# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FangCityItem(scrapy.Item):
    name = scrapy.Field()
    province = scrapy.Field()
    url = scrapy.Field()
    new_house_url = scrapy.Field()
    second_hand_url = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()


class FangFangItem(scrapy.Item):
    name = scrapy.Field()
    alias_name = scrapy.Field()
    arg_price = scrapy.Field()
    hotline = scrapy.Field()
    main_unit_type = scrapy.Field()
    user_rate = scrapy.Field()
    property = scrapy.Field()
    project_feature = scrapy.Field()
    construct_type = scrapy.Field()
    decoration_status = scrapy.Field()
    right_years = scrapy.Field()
    loop_position = scrapy.Field()
    developers = scrapy.Field()
    build_address = scrapy.Field()
    sale_status = scrapy.Field()
    property_concessions = scrapy.Field()
    open_time = scrapy.Field()
    delivery_time = scrapy.Field()
    traffic_condition = scrapy.Field()
    project_support = scrapy.Field()
    area = scrapy.Field()
    construct_area = scrapy.Field()
    volume_rate = scrapy.Field()
    green_rate = scrapy.Field()
    park_space = scrapy.Field()
    total_build = scrapy.Field()
    total_house = scrapy.Field()
    property_company = scrapy.Field()
    property_costs = scrapy.Field()
    floor_condition = scrapy.Field()
    project_desc = scrapy.Field()
    city_id = scrapy.Field()
    city_name = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    sale_address = scrapy.Field()
    house_type_url_id = scrapy.Field()

class XiechengCityItem(scrapy.Item):
    name = scrapy.Field()
    short_name = scrapy.Field()
    city_id = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    type = scrapy.Field()
    sub_city_name = scrapy.Field()
    sub_city_short_name = scrapy.Field()
    sub_city_id = scrapy.Field()

class XiechengSqItem(scrapy.Item):
    name = scrapy.Field()
    city_name = scrapy.Field()
    city_id = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    desc = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    path = scrapy.Field()
    sub_city_name = scrapy.Field()

class CleanHouseResItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    city_name = scrapy.Field()
    proj_desc = scrapy.Field()
    is_second_house = scrapy.Field()
    create_time = scrapy.Field()

