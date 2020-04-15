# -*- coding: utf-8 -*-
import scrapy
# from mfw_pic_sample.items import MfwPicSampleItem
import re

from scrapy.shell import inspect_response

class MfwSpider(scrapy.Spider):
    name = "mfw"
    allowed_domains = ["mafengwo.cn"]
    start_urls = ['http://www.mafengwo.cn']
    domain = 'http://www.mafengwo.cn'

    def parse(self, response):
        for image_item in response.xpath('//img'):
            yield {'image_urls': image_item.xpath('./@data-src').extract() }

        links = re.findall('href="(/i/\d+?.html)"', response.text)
        # inspect_response(response, self)

        for link in links:
            print 'append ' + link
            request = scrapy.Request( self.domain + link, callback=self.parse)
            yield request

        print ' ------ %s' % response.url
        page = response.url.split("/")[-1]
        filename = 'mfw-%s' % page
        with open(filename, 'wb') as f:
            f.write(response.body)