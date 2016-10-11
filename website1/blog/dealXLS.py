# -*- coding: utf-8 -*-
from xlrd import open_workbook
import xlwt
import httplib2
import re
import time
import urllib2
XLS_PATH="aa.xlsx"
DOWN_PATH = "result.xls"
data_list=range(1,1000)
start_time = time.time()
all_info_list = []
def read_xls(path):
    wb1 = open_workbook(unicode(path))
    wb = xlwt.Workbook()
    n=0
    for s in wb1.sheets():
        if s.nrows:
            nrows = s.nrows
        for num in range(s.nrows):
            values = s.row_values(num)
            values[2] = n
            all_info_list.append(values)
                #实现接口对接准备开爬
            n+=1
        return nrows,all_info_list
num,all_info_list=read_xls(XLS_PATH)
print "read over"
# print num,all_info_list
class AMZ(object):
    def __init__(self,info_list):
        self.asin = info_list[0]
        self.keyword = info_list[1]
        self.loc = info_list[2]
        self.product_name = ""
        self.rank = ""
        self.page_num = ""
        self.content_list=[self.asin,self.keyword,self.loc]

    def deal_url(self,url):
        headers = {
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Charset": "UTF-8;q=0.5",
          "Accept-Encoding": "gzip,deflate,sdch",
          "Accept-Language": "zh-CN,zh;q=0.8",
          "Cache-Control": "max-age=0",
          "Connection": "keep-alive",
          #"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91   Safari/534.30",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        }
        h = httplib2.Http()
        resp, content = h.request(url,headers=headers)

        return content
    def TestResult(self,result):
        #if 'height' and 'width' and 'Amazon' in result:
        if 'height' in result or 'Amazon ' in result:
            return False
        return True
    def get_product_name(self):
        url = 'http://www.amazon.de/gp/product/'+self.asin
        # print url
        content = self.deal_url(url)
        #pattern = re.compile('<img alt="(.*?)" src="',re.S)
        pattern = re.compile('<span id="productTitle" class="a-size-large">(.*?)</span>',re.S)
        result = re.findall(pattern,content)
        for i in result:
            if len(i)!=0:
                # i=i.replace("&#39;","'").replace("&amp;quot;",'"').replace("&quot;",'"').replace("&amp;","&")
                result=self.TestResult(i)
                if result:
                    #print "here"
                    self.product_name = i.replace("\n","").strip(" ")
                    return self.product_name
                return False

    def get_location(self,i):
        #product_name = self.get_product_name()

        # print i
        #print u'正在搜索第'+str(i)+u'页'
        url = 'https://www.amazon.de/s/ref=sr_pg_'+str(i)+'?rh=i%3Aaps%2Ck%3A'+self.keyword+'&page='+str(i)+'&keywords='+self.keyword
        url=url.replace(' ','+')
        #print url
        for i in range(10):
            content  = self.deal_url(url)
            # pattern = re.compile('<h2 data-attribute="(.*?)"',re.S)
            pattern = re.compile('<h2 data-attribute=".*?">(.*?)</h2>',re.S)
            result = re.findall(pattern,content)
            #print "all+"+str(len(result))
            print len(result)
            for x in result:
                print x
            if len(result)>28:
                break
        return result
            #开始比较
    def compare(self):
        product_name = self.get_product_name()
        for i in range(1,2):
            result = self.get_location(i)
            for product_item in result:
                # print product_item
                # if product_name==product_item:
                #     return "yes"
                if "..." in product_item:
                    if product_item[:-3] in self.product_name:
                        self.page_num = i
                        self.rank = result.index(product_item)+1
                        break
                if product_name==product_item:
                    self.page_num = i
                    self.rank = result.index(product_item)+1
                    break
            if self.rank:
                all_info_list[self.loc].append(str(self.page_num)+"page"+str(self.rank)+" row")
                # self.content_list.append(str(self.page_num)+"page"+str(self.rank))
                # data_list[self.loc] = self.content_list
                return str(self.page_num)+"page"+str(self.rank)
        # self.content_list.append("no find")
        # data_list[self.loc] = self.content_list
        #all_info_list[self.loc].append(str(self.page_num)+"page"+str(self.rank)+" row")
        all_info_list[self.loc].append("no find")
        return "no find"

# a = AMZ(['B014TE52RS','arduino nano',1])
# print a.compare()
# print all_info_list
for item in all_info_list[1:]:
    a = AMZ(item)
    a.compare()
    print "完成一个任务，正在继续下个查询"
# print all_info_list
#开始进行写操作：
wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet',cell_overwrite_ok=True)
ws.write(0,0,"ASIN")
ws.write(0,1,"kEYWORD")
ws.write(0,2,"RANK")
for item in all_info_list[1:]:
    row = item[2]#获取到第几行
    ws.write(row,0,item[0])
    ws.write(row,1,item[1])
    ws.write(row,2,item[3])
down_path = "111.xls"
wb.save(down_path) #修改
end_time = time.time()
print "over"
print "take all " +str(end_time-start_time) +" s"



