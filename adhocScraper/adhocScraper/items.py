# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose, Identity
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import re


class AdhocNewsItem(Item):
    newsID = Field(output_processor=TakeFirst())
    companyID = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())

    company_name = Field(
        input_processor=MapCompose(remove_tags, replace_entities),
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
        input_processor=MapCompose(remove_tags, replace_entities),
        output_processor=Join(),
    )
    text = Field(
        input_processor=MapCompose(remove_tags, replace_entities, lambda x: x.split()),
        output_processor=Join(),
    )
