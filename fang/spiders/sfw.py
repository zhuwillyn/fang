# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouseItem
from fang.items import ErShouFangItem

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    page = 1

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath("./td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s", "", province_text)
            if province_text:
                province = province_text
            if province == '其它':
                continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                url_module = city_url.split("//")
                scheme = url_module[0]
                domain = url_module[1]

                if 'bj.' in domain:
                    newhouse_url = "http://newhouse.fang.com/house/s/"
                    esf_url = "https://esf1.fang.com/"
                else:
                    newhouse_url = scheme + "//" + "newhouse." + domain + "house/s/"
                    esf_url = scheme + "//" + "esf." + domain

                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse, meta={"info": (province, city)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={"info": (province, city)})

    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class, 'nl_con')]/ul/li[not(@class)]/div[@class='clearfix']/div[@class='nlc_details']")
        for li in lis:
            item = NewHouseItem(province=province, city=city)
            ad = li.xpath(".//div[@class='nhouse_price']/em[2]/text()").get()
            if ad is not None:
                continue
            item['name'] = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            item['rooms'] = "/".join(li.xpath(".//div[contains(@class, 'house_type')]/a/text()").getall())
            item['area'] = re.sub(r"\s|/|－", "", "".join(li.xpath(".//div[contains(@class, 'house_type')]/text()").getall()))
            district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            item['district'] = re.search(r".*\[(.+)\].*", district_text).group(1)
            item['address'] = li.xpath(".//div[@class='address']/a/@title").get()
            item['origin_url'] = "http:{}".format(li.xpath(".//div[@class='nlcd_name']/a/@href").get())
            price_num = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            item['price'] = re.sub(r"\s", "", price_num)
            item['telephone'] = "".join(li.xpath(".//div[@class='tel']/p//text()").getall())
            item['sale'] = li.xpath(".//div[contains(@class, 'fangyuan')]/span/text()").get()
            item['label'] = "/".join(li.xpath(".//div[contains(@class, 'fangyuan')]/a/text()").getall())

            yield item

        # 分页请求
        span = response.xpath("//div[@class='otherpage']/span[1]/@class").get()
        if span == 'disable':
            next_page_url = response.xpath("//div[@class='otherpage']/a[1]/@href").get()
        else:
            next_page_url = response.xpath("//div[@class='otherpage']/a[2]/@href").get()

        if next_page_url is not None:
            next_page = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page, callback=self.parse_newhouse, meta={"info": (province, city)})

    def parse_esf(self, response):
        province, city = response.meta.get('info')
        houses = response.xpath("//div[contains(@class, 'shop_list')]/dl[contains(@dataflag, 'bg')]")
        for house in houses:
            item = ErShouFangItem(province=province, city=city)
            item['name'] = house.xpath(".//p[@class='add_shop']/a/@title").get()
            item['address'] = house.xpath(".//p[@class='add_shop']/span/text()").get()
            item['label'] = "/".join(house.xpath(".//p[contains(@class, 'label')]/span/text()").getall())
            item['total_price'] = "".join(house.xpath(".//dd[@class='price_right']/span[1]//text()").getall())
            item['price'] = house.xpath(".//dd[@class='price_right']/span[2]/text()").get()
            item['origin_url'] = response.urljoin(house.xpath(".//h4/a/@href").get())
            infos = house.xpath(".//p[@class='tel_shop']/text()").getall()
            house_infos = list(map(lambda x: re.sub(r"\s", "", x), infos))
            floor, year, toward = '', '', ''
            for house_info in house_infos:
                if '年建' in house_info:
                    year = re.sub(r"年建", "", house_info)
                elif re.search(r"室|厅", house_info):
                    item['rooms'] = house_info
                elif '层' in house_info:
                    floor = house_info
                elif '㎡' in house_info:
                    item['area'] = house_info
                elif '向' in house_info:
                    toward = house_info
                elif re.search(r"独栋|联排|花园", house_info):
                    floor += house_info + "/"
                elif re.search(r"卧室", house_info):
                    item['rooms'] = house_info
            item['floor'] = floor
            item['year'] = year
            item['toward'] = toward
            yield item

        # 获取下一页的url
        page_links = response.xpath("//div[@class='page_al']//a")
        for a_label in page_links:
            a_text = a_label.xpath("./text()").get()
            if a_text == '下一页':
                href = a_label.xpath("./@href").get()
                next_page_url = response.urljoin(href)
                yield scrapy.Request(url=next_page_url, callback=self.parse_esf, meta={"info": (province, city)})
                break

