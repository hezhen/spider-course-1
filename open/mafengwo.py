import urllib2
import json
from lxml import etree

request_headers = {
    'host': "www.mafengwo.cn",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
    'cookie': "mfw_uuid=5879e298-7d17-50bf-100a-30898d44da2d; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222017-01-14+16%3A34%3A32%22%3B%7D; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1484382875%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5879e298-7d17-50bf-100a-30898d44da2d; PHPSESSID=v17pef8jrto99pvsgsppo748j0; __mfwlv=1484402143; __mfwvn=2; __mfwlt=1484402151; uva=a%3A4%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1484402148%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22step%22%3Bi%3A9%3B%7D; CNZZDATA30065558=cnzz_eid%3D55928032-1484382591-%26ntime%3D1484397604",
    'postman-token': "0d7a1e08-f8d5-ec1f-ab2e-879ab9a00d34"
}

filename = 'mafengwo.html'
html_page = ''

try:
    fo = open(filename, 'r')
except IOError:
    req = urllib2.Request("http://www.mafengwo.cn", headers=request_headers)
    response = urllib2.urlopen(req)
    html_page = response.read()
    print html_page
    fo = open(filename, 'wb+')
    fo.write(html_page)

html_page = fo.read()

out_file = open("links.txt", "wb")

html = etree.HTML(html_page.lower().decode('utf-8'))
hrefs = html.xpath(u"//a")

for href in hrefs:
    if 'href' in href.attrib:
        val = href.attrib['href']
        if val.find('javascript:') != -1:
            continue
        if val.startswith('http://') is False:
            if val.startswith('/'):
                val = 'http://www.mafengwo.cn' + val
            else:
                continue
        out_file.write("%s\r\n" % (val.encode('utf-8')))

fo.close()
out_file.close()
