# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from ..items import ScrapyPicItem
from scrapy.selector import Selector
from ..items import TaoTuLinkItem
from scrapy.linkextractors import LinkExtractor
import scrapy

next_page = u"››"


class MiMiSpider(CrawlSpider):
    name = "mimi"
    allowed_domains = ["mimilol.com", "mmvrs.com"]
    start_urls = [
        "http://www.mmvrs.com/forumdisplay.php?fid=59"
    ]

    def parse_image(self, response):
        img_item = ScrapyPicItem()
        sel = Selector(response)
        image_urls = []
        img_item["image_dir"] = sel.xpath("//title/text()").extract()[0].split("-")[0]
        print img_item["image_dir"]
        for img in sel.css(".t_msgfont").xpath("./img/@src"):
            image_urls.append(img.extract())

        img_item["image_urls"] = image_urls
        yield img_item

    def parse(self, response):
        sel = Selector(response)
        for items in sel.css(".f_title").xpath("./a/@href"):
            result = items.extract()
            if result is not None and "redirect.php" not in result:
                next_request = response.urljoin(result)
                yield scrapy.Request(next_request, callback=self.parse_image)

        try:
            # next_request = sel.css(".p_redirect").xpath("./@href").extract()[0]
            next_request = sel.xpath("//a[text()='%s']/@href" % next_page).extract()[0]
        except Exception as exc:
            pass
        else:
            if next_request is not None:
                next_request = response.urljoin(next_request)
                yield scrapy.Request(next_request, callback=self.parse)
