# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名称
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 房屋格局
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 详情页面url
    origin_url = scrapy.Field()
    # 电话
    telephone = scrapy.Field()
    label = scrapy.Field()

class ErShouFangItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名称
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 总价
    total_price = scrapy.Field()
    # 房屋格局
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    floor = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 详情页面url
    origin_url = scrapy.Field()
    label = scrapy.Field()
    toward = scrapy.Field()
    year = scrapy.Field()
