# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose, Identity
from w3lib.html import remove_tags
import re


class AdhocNewsItem(scrapy.Item):
    url = Field()

    company_name = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    wkn = Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
    )
    isin = Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
    )
    country = Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
    )
    timestamp = Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
    )
    headline = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    text = Field(
        input_processor=MapCompose(remove_tags, lambda x: x.split()),
        output_processor=Join(),
    )
