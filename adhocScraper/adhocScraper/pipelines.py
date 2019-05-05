# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import FilesPipeline

class AdhocscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class ArivaFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        print('item-isin:', item['isin'])
        return [scrapy.Request(x, meta={'isin': item['isin']}) for x in item.get('file_urls', [])]

    def file_path(self, request, response=None, info=None):
        return 'isin_%s.csv' % request.meta.get('isin')
