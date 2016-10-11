
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import httplib2
import requests
from lxml import etree
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import time
def getProductName(asin):
    url = 'http://www.amazon.it/gp/product/'+str(asin)
    print url
    try:#Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0
        print u"为什么这么慢"
        headers = {
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Charset": "UTF-8;q=0.5",
          "Accept-Encoding": "gzip,deflate,sdch",
          "Accept-Language": "zh-CN,zh;q=0.8",
          "Cache-Control": "max-age=0",
          "Connection": "keep-alive",
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91   Safari/534.30",
        }
        h = httplib2.Http(".cache")
        resp, content = h.request(url,headers=headers)
        # print resp,'\n\n\n\n\n',content
           # page = response.read()
        print "sdd"
        # pattern = re.compile('<span id="productTitle" class="a-size-large">(.*?)</span>',re.S)
        # result = re.findall(pattern,content)
        # print "ok"
        # print result
        # if not result:

        #pattern = re.compile('<title>.*?: (.*?):',re.S)
        # pattern = re.compile('<title>(.*?):',re.S)
        # result = re.findall(pattern,content)
        # print result[0]
        # if "&" in result[0]:
        #     pattern = re.compile('<img alt="(.*?)" src="',re.S)
        #     result = re.findall(pattern,content)
        #     print result[1]
        #     # if result[1] =='iCreation i-450 Docking Station für Apple iPhone weiß':
        #     #
        #     #     print '2222222'
        #     return result[1]
        #
        # if "&quot" in result[0]:
        #     print result[0].replace("&quot;",'"')
        #     return result[0].replace("&quot;",'"')
        # return result[0]
        pattern = re.compile('<img alt="(.*?)" src="',re.S)
        result = re.findall(pattern,content)
        for i in result:
            if len(i)!=0:
                print i
                return i

    except urllib2.URLError, e:
        if hasattr(e,"reason"):
            print u"查找商品名失败,错误原因",e.reason
            return None


s1 = time.time()
getProductName('B01CS8I4F4')
s2 = time.time()
print s2-s1

