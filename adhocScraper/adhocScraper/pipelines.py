# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from arctic import CHUNK_STORE, Arctic
from scrapy.contrib.pipeline.images import FilesPipeline


# from scrapy.exceptions import DropItem
#
#
# class DuplicatesPipeline(object):
#
#     def __init__(self):
#         self.ids_seen = set()
#
#     def process_item(self, item, spider):
#         if item['id'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['id'])
#             return item

# TODO: Either create CSV pipeline to append to existing file for Adhoc announcements or DB to read from & append to
class AdhocscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class ArivaFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        print('item-isin:', item['isin'])
        return [scrapy.Request(x, meta={'isin': item['isin']}) for x in item.get('file_urls', [])]

    def file_path(self, request, response=None, info=None):
        return 'isin_%s.csv' % request.meta.get('isin')


class ArcticPipeline(object):

    # collection_name = 'scrapy_items'

    def __init__(self, arctic_uri, arctic_store):
        self.arctic_uri = arctic_uri
        self.arctic_store = arctic_store

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            arctic_uri=crawler.settings.get('ARCTIC_URI'),
            arctic_store=crawler.settings.get('ARCTIC_STORE')
        )

    def open_spider(self, spider):
        self.client = Arctic(self.arctic_uri)
        self.db = self.client.initialize_library(self.arctic_store, lib_type=CHUNK_STORE)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # self.db[self.collection_name].insert_one(dict(item))
        return item
