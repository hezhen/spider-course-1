# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from ..items import ScrapyPicItem
from scrapy.selector import Selector
from ..items import TaoTuLinkItem
from scrapy.linkextractors import LinkExtractor
import scrapy

next_page = u"下一页"


class TaoTuSpider(CrawlSpider):
    name = "taotu"
    allowed_domains = ["aitaotu.com"]
    start_urls = [
        "http://www.aitaotu.com/tag/meituibaobei.html"
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
        taotu_link_item = TaoTuLinkItem()
        sel = Selector(response)
        # next_page = u"下一页"
        for items in sel.xpath('//div[@id="mainbody"]/ul[@id="mainbodypul"]/li/a/@href'):
            item_link = "%s%s" % ("http://www.aitaotu.com", items.extract())
            yield scrapy.Request(item_link, callback=self.parse_image)

        try:
            next_request = sel.xpath("//a[text()='%s']/@href" % next_page).extract()[0]
        except Exception:
            pass
        else:
            if next_request is not None:
                next_request = response.urljoin(next_request)
                yield scrapy.Request(next_request, callback=self.parse)
