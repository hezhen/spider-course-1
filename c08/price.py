import signal
from lxml import etree

from selenium import webdriver
import selenium
import re

# custom header
headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Charset':'utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Connection': 'keep-alive'
    }

# set custom headers
for key, value in headers.iteritems():
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

# another way to set custome header
webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = \
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'


jd_item_url = 'https://item.jd.com/2131674.html'

# get item id by regualar expression
item_id = re.findall('/\d{7}.html', jd_item_url)[0][1:8]

# ignore ssl error, optionally can set phantomjs path
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true']) # or add to your PATH

# set bigger windows height to dynamically load more data
driver.set_window_size(1280, 2400) # optional
driver.get(jd_item_url)

# driver.execute_script('window.scrollTo(0, (document.body.scrollHeight))')
# driver.save_screenshot('screen.png') # save a screenshot to disk

max_try = 2
num_try = 0

# ajax could be slow, so we should wait and try several times expected element data are loaded
while num_try < max_try:
    try:
        element = driver.find_element_by_class_name('rate')
        print element.find_element_by_tag_name('strong').text
        price_element = driver.find_element_by_class_name('J-p-%s'%(item_id))
        print re.findall('\d.*', price_element.get_attribute('innerHTML'))[0]
        break
    except selenium.common.exceptions.NoSuchElementException, Arguments:
        num_try += 1
        print Arguments

print 'items:'
for url in re.findall('href="//item.jd.com/\d{7}.html"', driver.page_source):
    print url

print '\n\nlists:'
for url in re.findall('href="//list.jd.com/list.html.*\d{3,5}"', driver.page_source):
    print url

# use page_source to get rendered content page
# f = open(jd_item_url[8:].replace('/','_'), 'wb+')
# f.write(driver.page_source.encode('utf-8'))
# f.close()

# to properly close phantomjs, call one of below 2 methods send_signal or close()
# 1. send_signal is recommended
# driver.service.process.send_signal(signal.SIGTERM)
# 2. or use close() but close() is not guaranteed
driver.close()

driver.quit()

# to assure it's closed, run below command in terminal
# pgrep phantomjs | xargs kill