# -*- coding: utf-8 -*-
import json

from scrapy.contrib.spiders import CrawlSpider, Rule
from ..items import ScrapyPicItem
from scrapy.selector import Selector
from ..items import TaoTuLinkItem
from scrapy.linkextractors import LinkExtractor
import scrapy
import re

next_page = u"下一页"


class BaiduSpider(CrawlSpider):
    name = "baidu"
    allowed_domains = ["baidu.com", "bdimg.com"]
    start_urls = [
        "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E8%83%8C%E5%8C%85&ct=201326592&v=flip"
    ]
    # rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[text() = '%s']/@href" % next_page)), callback="parse",
    #               follow=True),)

    def parse_image(self, response):
        img_item = ScrapyPicItem()
        sel = Selector(response)
        image_urls = []
        for img in sel.xpath('(//div)[@id="big-pic"]/p/a/img/@src'):
            image_urls.append(img.extract())

        img_item["image_urls"] = image_urls
        yield img_item

        try:
            next_request = sel.xpath("//a[text()='%s']/@href" % next_page).extract()[0]
        except Exception:
            pass
        else:
            if next_request is not None:
                next_request = response.urljoin(next_request)
                yield scrapy.Request(next_request, callback=self.parse_image)

    def parse(self, response):
        img_item = ScrapyPicItem()
        sel = Selector(response)
        print sel.xpath("//title/text()").extract()[0]
        # p = re.compile('"thumbURL":".*"')
        p = re.compile('"data":\[.*\]')
        result = p.search(response.body)
        tmp = result.group(0).split('"data":')[1]
        img_list = json.loads(tmp)
        img_urls = []
        for i in img_list:
            print i.get("thumbURL", "")
            img_url = i.get("thumbURL", "")
            if img_url:
                img_urls.append(img_url)

        img_item["image_urls"] = img_urls
        yield img_item
        # print result.group(0)
        # for i in result:
        #     print i
        # match = re.findall('"thumbURL": "(\w+)"', response.body)
        # print match
        # for items in sel.css(".imgbox").xpath("./a/img/@src"):
        #     print items.extract()
        # taotu_link_item = TaoTuLinkItem()
        # sel = Selector(response)
        # # next_page = u"下一页"
        # for items in sel.xpath('//div[@id="mainbody"]/ul[@id="mainbodypul"]/li/a/@href'):
        #     item_link = "%s%s" % ("http://www.aitaotu.com", items.extract())
        #     yield scrapy.Request(item_link, callback=self.parse_image)
        #
        # try:
        #     next_request = sel.xpath("//a[text()='%s']/@href" % next_page).extract()[0]
        # except Exception:
        #     pass
        # else:
        #     if next_request is not None:
        #         next_request = response.urljoin(next_request)
        #         yield scrapy.Request(next_request, callback=self.parse)
