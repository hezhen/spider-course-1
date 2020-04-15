# -*- coding: utf-8 -*-
import scrapy


class Qy01Spider(scrapy.Spider):
    name = "qy01"
    allowed_domains = ["qiongyou.com"]
    start_urls = ['http://qiongyou.com/']

    def parse(self, response):
        pass
