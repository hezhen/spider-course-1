# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyPicItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_dir = scrapy.Field()
    image_paths = scrapy.Field()
    next_paths = scrapy.Field()


class TaoTuLinkItem(scrapy.Item):
    item_link = scrapy.Field()
