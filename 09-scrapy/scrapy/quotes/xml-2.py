from scrapy.spiders import XMLFeedSpider

class MySpider(XMLFeedSpider):
    name = 'mfwsitemap'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://www.mafengwo.cn/sitemapIndex.xml']
    iterator = 'html'
    itertag = 'sitemap' # the tag name of node

    def parse_node(self, response, node):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        
        item = {}
        item['loc'] = node.xpath('loc').extract()
        item['lastmod'] = node.xpath('lastmod').extract()
        return item