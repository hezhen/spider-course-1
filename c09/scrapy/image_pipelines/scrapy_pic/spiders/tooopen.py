# -*- coding: utf-8 -*-
import json

from scrapy.contrib.spiders import CrawlSpider, Rule
from ..items import ScrapyPicItem
from scrapy.selector import Selector
from ..items import TaoTuLinkItem
from scrapy.linkextractors import LinkExtractor
import scrapy
import re

next_page = u">"

search_names = [
    u"狗狗图片",
    u"猫咪图片",
    u"兔子图片",
    u"鸽子图片",
    u"骏马图片",
    u"老虎图片",
    u"大熊猫图片",
    u"大象图片",
    u"鲸鱼图片",
]


class TooOpenSpider(CrawlSpider):
    name = "tooopen"
    allowed_domains = ["tooopen.com"]
    start_urls = [
        "http://www.tooopen.com/img/89.aspx",
    ]
    # rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[text() = '%s']/@href" % next_page)), callback="parse",
    #               follow=True),)

    def parse_image(self, response):
        img_item = ScrapyPicItem()
        sel = Selector(response)
        image_urls = []
        for img in sel.css(".cell").xpath('./a/img/@src'):
            print img.extract()
            # image_urls.append(img.extract())

        # img_item["image_urls"] = image_urls
        # yield img_item
        #
        # try:
        #     next_request = sel.xpath("//a[text()='%s']/@href" % next_page).extract()[0]
        # except Exception:
        #     pass
        # else:
        #     if next_request is not None:
        #         next_request = response.urljoin(next_request)
        #         yield scrapy.Request(next_request, callback=self.parse_image)

    def parse_single(self, response):
        img_item = ScrapyPicItem()
        image_urls = []
        sel = Selector(response)
        img_item["image_dir"] = sel.xpath("//title/text()").extract()[0].split(",")[0]
        for img in sel.css(".cell").xpath('./a/img/@src'):
            image_urls.append(img.extract())
        img_item["image_urls"] = image_urls
        yield img_item

        try:
            next_request = sel.css(".border-r").xpath("@href").extract()[0]
        except Exception as exc:
            pass
        else:
            if next_request is not None:
                next_request = response.urljoin(next_request)
                yield scrapy.Request(next_request, callback=self.parse_single)

    def parse(self, response):
        # img_item = ScrapyPicItem()
        # image_urls = []
        sel = Selector(response)
        # for img in sel.css(".cell").xpath('./a/img/@src'):
        #     image_urls.append(img.extract())
        # img_item["image_urls"] = image_urls
        # yield img_item
        for i in search_names:
            try:
                next_request = sel.xpath("//a[text()='%s']/@href" % i).extract()[0]
            except Exception as exc:
                pass
            else:
                if next_request is not None:
                    next_request = response.urljoin(next_request)
                    yield scrapy.Request(next_request, callback=self.parse_single)

