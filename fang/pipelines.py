# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
from fang.items import ErShouFangItem, NewHouseItem
from scrapy.exporters import JsonLinesItemExporter


class FangPipeline(object):

    def __init__(self):
        self.newhouse_fp = open('newhouse.json', 'w')
        self.esfhouse_fp = open('ershouse.json', 'w')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp, ensure_ascii=False, encoding='utf-8')
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.newhouse_exporter.export_item(item)
        elif isinstance(item, ErShouFangItem):
            self.esfhouse_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()


class ExportExcelPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['省份', '城市', '行政区', '小区名称', '格局', '面积', '总价', '地址', '是否在售', '特点', '电话', '链接'])

        self.esfhouse_wb = Workbook()
        self.esfhouse_ws = self.esfhouse_wb.active
        self.esfhouse_ws.append(['省份', '城市', '小区名称', '年份', '格局', '面积', '总价', '单价', '层高', '地址', '朝向', '备注', '链接'])

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            newhouse_item = [item['province'],
                             item['city'],
                             item['district'],
                             item['name'],
                             item['rooms'],
                             item['area'],
                             item['price'],
                             item['address'],
                             item['sale'],
                             item['label'],
                             item['telephone'],
                             item['origin_url']]
            self.ws.append(newhouse_item)
        elif isinstance(item, ErShouFangItem):
            erfhouse_item = [item['province'],
                    item['city'],
                    item['name'],
                    item['year'],
                    item['rooms'],
                    item['area'],
                    item['total_price'],
                    item['price'],
                    item['floor'],
                    item['address'],
                    item['toward'],
                    item['label'],
                    item['origin_url']]
            self.esfhouse_ws.append(erfhouse_item)
        return item

    def close_spider(self, spider):
        self.wb.save('全国新房信息.xlsx')
        self.esfhouse_wb.save('全国二手房信息.xlsx')
