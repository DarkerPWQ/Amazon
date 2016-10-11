# -*- coding: utf-8 -*-
import urllib2
import re
import httplib2
import operator
import xlrd
import xlwt
def get_page(url):
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

    return content