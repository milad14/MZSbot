# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


def attach_reuters_url(value):
    name = 'https://www.reuters.com'
    return name + value

class ReutersItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    summary = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    date = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    link = scrapy.Field(
        input_processor = MapCompose(attach_reuters_url),
        output_processor = TakeFirst()
    )

'''
class EuroNewsItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    summary = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    date = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    link = scrapy.Field(
        input_processor = MapCompose(attach_reuters_url),
        output_processor = TakeFirst()
    )
'''
