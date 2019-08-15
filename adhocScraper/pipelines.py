# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from os.path import isfile
import scrapy
from scrapy.contrib.pipeline.images import FilesPipeline
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
import pandas as pd


class ArivaCompanyMetaDataDuplicatesPipeline(object):

    def __init__(self, filepath, filename):
        try:
            self.file = pd.read_csv(filepath)
            self.ids_seen = set(self.file['isin'])
        except FileNotFoundError:
            self.ids_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            filepath=crawler.settings.get('ARIVA_METADATA_FILEPATH', ''),
            filename=crawler.settings.get('ARIVA_METADATA_FILENAME', '')
        )

    def process_item(self, item, spider):
        if item['isin'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['isin'])
            return item


class AdhocAnnouncementsDuplicatesPipeline(object):

    def __init__(self, filepath, filename):
        try:
            self.file = pd.read_csv(filepath)
            self.ids_seen = set(self.file['newsID'])
        except FileNotFoundError:
            self.ids_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            filepath=crawler.settings.get('ADHOC_FILEPATH', ''),
            filename=crawler.settings.get('ADHOC_FILENAME', '')
        )

    def process_item(self, item, spider):
        if item['newsID'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['newsID'])
            return item


class CSVPipeline(object):
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        self.file = None
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        raise NotImplementedError

    def open_spider(self, spider):
        file_exists = isfile(self.filepath)
        self.file = open(self.filepath, 'ab')
        # TODO: Add file paths with pathlib
        self.exporter = CsvItemExporter(self.file, include_headers_line=False if file_exists else True)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class AdhocAnnouncementsCSVPipeline(CSVPipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            filepath=crawler.settings.get('ADHOC_FILEPATH', ''),
            filename=crawler.settings.get('ADHOC_FILENAME', '')
        )


class ArivaCompanyMetadataCSVPipeline(CSVPipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            filepath=crawler.settings.get('ARIVA_METADATA_FILEPATH', ''),
            filename=crawler.settings.get('ARIVA_METADATA_FILENAME', '')
        )


class ArivaFilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        print('item-isin:', item['isin'])
        return [scrapy.Request(x, meta={'isin': item['isin']}) for x in item.get('file_urls', [])]

    def file_path(self, request, response=None, info=None):
        return 'isin_%s.csv' % request.meta.get('isin')
