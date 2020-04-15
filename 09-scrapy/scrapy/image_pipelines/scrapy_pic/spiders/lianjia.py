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


class LianJiaSpider(CrawlSpider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    start_urls = [
        "http://bj.lianjia.com/ershoufang/rs%E7%87%95%E9%83%8A/"
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

    def parse_price(self, response):
        sel = Selector(response)
        for items in sel.css(".info"):
            try:
                house_location = items.css(".houseInfo").xpath("./a/text()").extract()[0]
                houseInfo = items.css(".houseInfo").xpath("text()").extract()[0]
                total_price = items.css(".totalPrice").xpath("./span/text()").extract()[0]
                unit_price = items.css(".unitPrice").xpath("./span/text()").extract()[0]
                unit_price = int(re.findall(r'[\d|.]+', unit_price)[0])
                house_size = float(re.findall(r'[\d|.]+', houseInfo.split("|")[2])[0])
            except Exception as exc:
                pass
            else:
                print house_location, house_size, u"总价", total_price, u"单价", unit_price

    def parse(self, response):
        sel = Selector(response)

        page_data = sel.css(".page-box div::attr(page-data)").extract()[0]
        page_url = "%s" % sel.css(".page-box div::attr(page-url)").extract()[0]
        page_data = json.loads(page_data)
        page_count = int(page_data.get("totalPage", 1))
        for i in range(1, page_count+1):
            tmp = page_url.replace("{page}", str(i))
            next_request = response.urljoin(tmp)
            yield scrapy.Request(next_request, callback=self.parse_price)
