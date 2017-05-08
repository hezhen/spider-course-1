import urllib2
from collections import deque
import json
from lxml import etree
import httplib
import hashlib
from pybloomfilter import BloomFilter

class CrawlBSF:
    request_headers = {
        'host': "www.mafengwo.cn",
        'connection': "keep-alive",
        'cache-control': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
        }

    cur_level = 0
    max_level = 5
    dir_name = 'iterate/'
    iter_width = 50
    downloaded_urls = []

    du_md5_file_name = dir_name + 'download.txt'
    du_url_file_name = dir_name + 'urls.txt'

    download_bf = BloomFilter(1024*1024*16, 0.01)

    cur_queue = deque()
    child_queue = deque()

    def __init__(self, url):
        self.root_url = url
        self.cur_queue.append(url)
        self.du_file = open(self.du_url_file_name, 'a+')
        try:
            self.dumd5_file = open(self.du_md5_file_name, 'r')
            self.downloaded_urls = self.dumd5_file.readlines()
            self.dumd5_file.close()
            for urlmd5 in self.downloaded_urls:
                self.download_bf.add(urlmd5[:-2])
        except IOError:
            print "File not found"
        finally:
            self.dumd5_file = open(self.du_md5_file_name, 'a+')

    def enqueueUrl(self, url):
        self.child_queue.append(url)

    def dequeuUrl(self):
        try:
            url = self.cur_queue.popleft()
            return url
        except IndexError:
            self.cur_level += 1
            if self.cur_level == self.max_level:
                return None
            if len(self.child_queue) == 0:
                return None
            self.cur_queue = self.child_queue
            self.child_queue = deque()
            return self.dequeuUrl()

    def getpagecontent(self, cur_url):
        print "downloading %s at level %d" % (cur_url, self.cur_level)
        try:
            req = urllib2.Request(cur_url, headers=self.request_headers)
            response = urllib2.urlopen(req)
            html_page = response.read()
            filename = cur_url[7:].replace('/', '_')
            fo = open("%s%s.html" % (self.dir_name, filename), 'wb+')
            fo.write(html_page)
            fo.close()
        except urllib2.HTTPError, Arguments:
            print Arguments
            return
        except httplib.BadStatusLine:
            print 'BadStatusLine'
            return
        except IOError:
            print 'IO Error at ' + filename
            return
        except Exception, Arguments:
            print Arguments
            return
        # print 'add ' + hashlib.md5(cur_url).hexdigest() + ' to list'
        dumd5 = hashlib.md5(cur_url).hexdigest()
        self.downloaded_urls.append(dumd5)
        self.dumd5_file.write(dumd5 + '\r\n')
        self.du_file.write(cur_url + '\r\n')
        self.download_bf.add(dumd5)

        html = etree.HTML(html_page.lower().decode('utf-8'))
        hrefs = html.xpath(u"//a")

        for href in hrefs:
            try:
                if 'href' in href.attrib:
                    val = href.attrib['href']
                    if val.find('javascript:') != -1:
                        continue
                    if val.startswith('http://') is False:
                        if val.startswith('/'):
                            val = 'http://www.mafengwo.cn' + val
                        else:
                            continue
                    if val[-1] == '/':
                        val = val[0:-1]
                    # if hashlib.md5(val).hexdigest() not in self.downloaded_urls:
                    if hashlib.md5(val).hexdigest() not in self.download_bf:
                        self.enqueueUrl(val)
                    else:
                        print 'Skip %s' % (val)
            except ValueError:
                continue

    def start_crawl(self):
        while True:
            url = self.dequeuUrl()
            if url is None:
                break
            self.getpagecontent(url)
        self.dumd5_file.close()
        self.du_file.close()

crawler = CrawlBSF("http://www.mafengwo.cn")
crawler.start_crawl()