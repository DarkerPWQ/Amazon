
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render,HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader,Context
import datetime
import urllib2
import threading
from lxml import etree
import time
import httplib2
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
#from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from blog.models import *
#用户自定义扩展
from forms import *
# from django.contrib.auth.views import logout
from django.contrib.auth import authenticate,login
from django.contrib import auth
import random
from celery import task

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
@task()
def add():
    print "dijjdi"
#当settings.py中的djcelery.setup_loader()运行时, Celery便会查看所有INSTALLED_APPS中app目录中
# 的tasks.py文件, 找到标记为task的function, 并将它们注册为celery task
@task()
def add111():
    print "dijjdi"
@task()
def mul(x, y):
    print "%d * %d = %d"%(x,y,x*y)
    return x*y
@task()
def sub111(x, y):
    print "%d - %d = %d"%(x,y,x-y)
    return x-y
@task()
def everyday():#任务计划每天凌晨1分开始更新数据，与前一天有联系。
    print "ee"
    mylock = threading.RLock()
    class YMX(threading.Thread):
        def __init__(self,key,goods,num,country):#写反了，但不改了
            print u'第'+str(num)
            threading.Thread.__init__(self)
            self.basegood =unicode(goods)
            print
            self.basegood1 = '&keywords='+unicode(goods)
            # try:
            #     self.key = key.decode('gbk')#非常非常重要
            # except:
            #     self.key =key
            self.key =key
            baseURL='http://www.amazon.com/s/ref=sr_pg_1?rh=i%3Aaps%2Ck%3A'+self.basegood
            self.baseURL = baseURL
            self.success=0
            self.num = num
            self.a=""
            self.rank=0
            self.country=country
            self.items=0
        def getPage(self,url):
            try:
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
                resp, page = h.request(url,headers=headers)
                selector=etree.HTML(page)
                #content=selector.xpath('//h2[@class="a-size-medium a-color-null s-inline  s-access-title  a-text-normal"]/text()')
                result=[]
                for item in range(self.items,self.items+20):
                    string = '//li[@id="result_'+str(item)+'"]/div/div/div/div[2]/div[2]/a/h2/text()'
                    #print string
                    content=selector.xpath(string)
                    if(content):
                        result.append(content[0])
                self.items=self.items+len(result)
                print u'现在的'+str(self.items)


                # print u"结果"+ str(len(content))
                # #self.rank=self.ranklen(content)
                # #print str(len(content))+u'个'
                n = 0#真正商品的计数
                # if len(content)==0:
                #     headers = {
                #       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                #       "Accept-Charset": "UTF-8;q=0.5",
                #       "Accept-Encoding": "gzip,deflate,sdch",
                #       "Accept-Language": "zh-CN,zh;q=0.8",
                #       "Cache-Control": "max-age=0",
                #       "Connection": "keep-alive",
                #       "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91   Safari/534.30",
                # }
                #     h = httplib2.Http(".cache")
                #     resp, page = h.request(url,headers=headers)
                #     print u'重新'
                #     selector=etree.HTML(page)
                #     content=selector.xpath('//h2[@class="a-size-medium a-color-null s-inline  s-access-title  a-text-normal"]/text()')
                #     #print str(len(content))+u'个11'
                #     n = 0#真正商品的计数
                # if len(content)==0:
                #     headers = {
                #           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                #           "Accept-Charset": "UTF-8;q=0.5",
                #           "Accept-Encoding": "gzip,deflate,sdch",
                #           "Accept-Language": "zh-CN,zh;q=0.8",
                #           "Cache-Control": "max-age=0",
                #           "Connection": "keep-alive",
                #           "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91   Safari/534.30",
                #             }
                #     h = httplib2.Http(".cache")
                #     resp, html = h.request(url,headers=headers)
                #     print u'重新'
                #     selector=etree.HTML(html)
                #     content=selector.xpath('//h2[@class="a-size-medium a-color-null s-inline  s-access-title  a-text-normal"]/text()')
                #     print str(len(content))+u'个11'
                #     n = 0#真正商品的计数
                # print u'结果'+ str(len(content))
                for i in result:
                    self.rank+=1
                    n+=1
                    if '  ' in i:
                        if i.replace('  '," ") == self.key:
                            print u'已找到'
                            self.success=1
                            return n
                    if  '...' in i:
                        if i[:-3] in self.key:
                            print u'已找到'
                            self.success=1
                            return n

                    if i == self.key:
                        #print type(i)
                        print u'已找到'
                        self.success=1
                        return n
            except urllib2.URLError, e:
                if hasattr(e,"reason"):
                    print u"连接亚马逊失败,错误原因",e.reason
                    return None
            #在这里回忆下标准的正则表达的运用。可能与之前的不大一样，但这最基本的地方必须要知道如何书写：还有就是findall后产生的结果是list.
        def deal(self):
            #这里根据关键词和name
           # Result=Queryproducts.objects.filter(loginuser_id=Usernameobj.id).filter(productname = self.key).filter(querytime = nowtime)
            #print Result
            for i in range(1,7):
                # print i
                #print u'正在搜索第'+str(i)+u'页'
                url = 'http://www.amazon.'+str(self.country)+'/s/ref=sr_pg_'+str(i)+'?rh=i%3Aaps%2Ck%3A'+self.basegood+'&page='+str(i)+self.basegood1
                url=url.replace(' ','+')
                n = self.getPage(url)
                if self.success:
                    mylock.acquire()
                    Result=Queryproducts.objects.get(Asin =Asin,loginuser_id=loginuser_id,productname = self.key,querytime=nowtime_char,country = self.country)
                    self.a = u'在第'+str(i)+u'页的第'+ str(n) +u'个'
                    print self.a
                    if self.num==1:
                        Result.productrank1=self.a
                        Result.productindex1=self.rank
                        Result.flag1=1
                    elif self.num==2:
                        Result.productrank2=self.a
                        Result.productindex2=self.rank
                        Result.flag2=1
                    else:
                        Result.productrank3=self.a
                        Result.productindex3=self.rank
                        Result.flag3=1
                    Result.save()
                    mylock.release()

                    break
            if not self.success:
                mylock.acquire()
                Result=Queryproducts.objects.get(loginuser_id=loginuser_id,productname = self.key,querytime=nowtime_char,country = self.country)
                self.a = u'在六页以后'
                self.rank = ">100"
                print self.a
                if self.num==1:
                    Result.productrank1=self.a
                    Result.productindex1=self.rank
                    Result.flag1=1
                elif self.num==2:
                    Result.productrank2=self.a
                    Result.productindex2=self.rank
                    Result.flag2=1
                else:
                    Result.productrank3=self.a
                    Result.productindex3=self.rank
                    Result.flag3=1
                Result.save()
                mylock.release()

        def run(self):
            print 'MyThread1 starting','at:',time.ctime()
            self.res = apply(self.deal)
            #self.ws.save('C:\Users\pwq\Desktop\ymx1.xls')
            print 'finish at:',time.ctime()
    #获取昨天的
    q=str(datetime.datetime.now())[0:10]
    nowtime = datetime.datetime.strptime(q, "%Y-%m-%d")
    nowtime_char=str(nowtime)[0:10]#当前时间的字符串
    aftertime = nowtime - datetime.timedelta(days = 1)#获取昨天的时间
    aftertime_char=str(aftertime)[0:10]
    allProduct = Queryproducts.objects.filter(querytime = aftertime_char)#获取所有昨天的商品（通过昨天的时间）
    print len(allProduct)
    for i in allProduct:#遍历昨天的商品,i是Queryproduct的数据对象
        productname = i.productname
        loginuser_id = i.loginuser_id
        Asin = i.Asin
        country=i.country
        countryname= i.countryname
        productkeyword1 = i.productkeyword1
        productkeyword2 = i.productkeyword2
        productkeyword3 = i.productkeyword3
        productindex1 = i.productindex1
        productindex2 = i.productindex2
        productindex3 = i.productindex3
        Queryproducts.objects.create(Asin =Asin,productname =productname,productkeyword1=productkeyword1,
                                             productkeyword2=productkeyword2,productkeyword3=productkeyword3,loginuser_id=loginuser_id,querytime = nowtime_char,
                                     country = country,countryname = countryname)
        keyword=[]
        index_l=[]
        if productkeyword1:
            index_l.append(1)
            keyword.append(productkeyword1)
        if productkeyword2:
            keyword.append(productkeyword2)
            index_l.append(2)
        if productkeyword3:
            keyword.append(productkeyword3)
            index_l.append(3)
        thread_list=[]
        for i in keyword:
            a = index_l[keyword.index(i)]
            thread1 = YMX(productname,i,a,country)
            thread1.setDaemon(True)
            thread1.start()
            thread_list.append(thread1)
        for thread in thread_list:
            thread.join()
        #进行index计算
        now_obj=Queryproducts.objects.get(loginuser_id=loginuser_id,productname = productname,querytime = nowtime_char,Asin=Asin,country = country)
            #由于django不能设置默认值，减法在没有值得情况下会报错，所以现在判断对应前关键字是否存在。
        print u'设置开始'
        if now_obj.productkeyword1:
            if now_obj.productindex1!=">100":#查看现在是否由关键字1
                if productkeyword1 and productindex1!=">100":#是否昨天由关键字
                    try:
                        varyindex1=int(productindex1)-int(now_obj.productindex1)
                        if varyindex1>0:
                            pic1='up'
                            varyindex1 = u"上升"+str(varyindex1)

                        elif varyindex1==0:
                            pic1='wu'
                        else:
                            pic1='down'
                            varyindex1 = u"下降"+str(varyindex1)[1:]
                        now_obj.varyindex1=varyindex1
                        now_obj.pic1=pic1
                    except:
                        pass
                else:
                    now_obj.varyindex1=u'新进入排名区'
                    now_obj.pic1 = 'wu'
            else:
                print u"来了呀"
                now_obj.varyindex1=u'未进入排名区'
                now_obj.pic1 = 'wu'
        if now_obj.productkeyword2:
            if now_obj.productindex2!=">100":#查看现在是否由关键字1
                if productkeyword2 and productindex2!=">100":#是否昨天由关键字
                    try:
                        varyindex2=int(productindex2)-int(now_obj.productindex2)
                        if varyindex2>0:
                            pic2='up'
                            varyindex2 = u"上升"+str(varyindex2)

                        elif varyindex2==0:
                            pic2='wu'
                        else:
                            pic2='down'
                            varyindex2 = u"下降"+str(varyindex2)[1:]
                        now_obj.varyindex2=varyindex2
                        now_obj.pic2=pic2
                    except:
                        pass
                else:
                    now_obj.varyindex2=u'新进入排名区'
                    now_obj.pic2 = 'wu'
            else:
                print u"来了呀"
                now_obj.varyindex2=u'未进入排名区'
                now_obj.pic2 = 'wu'
        if now_obj.productkeyword3:
            if now_obj.productindex3!=">100":#查看现在是否由关键字1
                if productkeyword3 and productindex3!=">100":#是否昨天由关键字
                    try:
                        varyindex3=int(productindex3)-int(now_obj.productindex3)
                        if varyindex3>0:
                            pic3='up'
                            varyindex3 = u"上升"+str(varyindex3)

                        elif varyindex3==0:
                            pic3='wu'
                        else:
                            pic3='down'
                            varyindex3 = u"下降"+str(varyindex3)[1:]
                        now_obj.varyindex3=varyindex3
                        now_obj.pic3=pic3
                    except:
                        pass
                else:
                    now_obj.varyindex3=u'新进入排名区'
                    now_obj.pic3 = 'wu'
            else:
                print u"来了呀"
                now_obj.varyindex3=u'未进入排名区'
                now_obj.pic3 = 'wu'
        now_obj.save()
@task
def dealxls(file_name,user,country):
    import time
    import threading
    import urllib2
    import re
    from lxml import etree
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    def TestResult(result):
        print "22222222222"
        if 'height' and 'width' and 'Amazon' in result:
            return False
        return True
    def getProductName(asin,country):
        url = 'http://www.amazon.'+str(country)+'/gp/product/'+str(asin)
        print url
        try:
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
            h = httplib2.Http()
            resp, content = h.request(url,headers=headers)

            pattern = re.compile('<img alt="(.*?)" src="',re.S)
            result = re.findall(pattern,content)
            for i in result:
                if len(i)!=0:
                    #print i
                    i=i.replace("&#39;","'").replace("&amp;quot;",'"').replace("&quot;",'"').replace("&amp;","&")
                    result=TestResult(i)
                    if result:
                        print "here"
                        return i
                    return False
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"查找商品名失败,错误原因",e.reason
                return None
    class YMX(threading.Thread):
        def __init__(self,productName,key,row,num,ws,country):#写反了，但不改了
            print u'第'+str(num)
            threading.Thread.__init__(self)
            self.basegood =unicode(key)
            self.basegood1 = '&keywords='+unicode(key)
            print "22222"
            self.productName =productName
            self.ws = ws
            self.country = country
            self.success=0
            self.num = num
            self.a=""
            self.rank=0
            self.row=row
            self.items=0
        def getPage(self,url):
            try:
                headers = {
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "Accept-Charset": "UTF-8;q=0.5",
                  "Accept-Encoding": "gzip,deflate,sdch",
                  "Accept-Language": "zh-CN,zh;q=0.8",
                  "Cache-Control": "max-age=0",
                  "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91   Safari/534.30",
                }
                h = httplib2.Http()
                resp, page = h.request(url,headers=headers)
                selector=etree.HTML(page)
                result=[]
                for item in range(self.items,self.items+20):
                    string = '//li[@id="result_'+str(item)+'"]/div/div/div/div[2]/div[2]/a/h2/text()'
                    #print string
                    content=selector.xpath(string)
                    if(content):
                        result.append(content[0])
                self.items=self.items+len(result)
                print u'现在的'+str(self.items)


                #self.rank=self.ranklen(content)
                #print str(len(content))+u'个'
                n = 0#真正商品的计数
                for i in result:
                    self.rank+=1
                    n+=1
                    if '  ' in i:
                        if i.replace('  '," ") == self.productName:
                            print u'已找到'
                            self.success=1
                            return n
                    if  '...' in i:
                        if i[:-3] in self.productName:
                            print u'已找到'
                            self.success=1
                            return n
                    if i == self.productName:
                        #print type(i)
                        print u'已找到'
                        self.success=1
                        return n
            except urllib2.URLError, e:
                if hasattr(e,"reason"):
                    print u"连接亚马逊失败,错误原因",e.reason
                    return None
            #在这里回忆下标准的正则表达的运用。可能与之前的不大一样，但这最基本的地方必须要知道如何书写：还有就是findall后产生的结果是list.
        def deal(self):
            for i in range(1,7):
                #print u'正在搜索第'+str(i)+u'页'
                url = 'http://www.amazon.'+str(self.country)+'/s/ref=sr_pg_'+str(i)+'?rh=i%3Aaps%2Ck%3A'+self.basegood+'&page='+str(i)+self.basegood1
                #print url
                n = self.getPage(url)
                if self.success:
                    #print '??'
                    a = u'在第'+str(i)+u'页的第'+ str(n) +u'个'
                    print a
                    self.ws.write(self.row,self.num,a)
                    break
            if not self.success:
                b=  u'在六页以后'
                print b
                self.ws.write(self.row,self.num,b)
        def run(self):
            print 'MyThread1 starting','at:',time.ctime()
            self.res = apply(self.deal)
            #self.ws.save('C:\Users\pwq\Desktop\ymx1.xls')
            print 'finish at:',time.ctime()
    from xlrd import open_workbook
    import xlwt
    starttime=time.time()
    i=file_name #修改
    print i
    wb1 = open_workbook(unicode(i))

    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet',cell_overwrite_ok=True)
    productname=[]
    Asin=[]
    key1=[]
    key2=[]
    key3=[]
    for s in wb1.sheets():
        if s.nrows:
            nrows = s.nrows
        for c in s.col_values(0):# 获取整列的值（数组）,所有的商品名称与关键词都准备就绪
            Asin.append(c)
        for c2 in s.col_values(2):
            key1.append(c2)
        for c3 in s.col_values(3):
            key2.append(c3)
        for c4 in s.col_values(4):
             key3.append(c4)
                #实现接口对接准备开爬
             for row in range(s.nrows):
                 for col in range(s.ncols):
                     i=s.cell(row,col).value
                     ws.write(row,col,i) #复制信息
    print u"到这里？"
    productname.append(" ")
    for asin in Asin[1:]:#
        name = getProductName(asin,country)
        index1=Asin.index(asin)
        ws.write(index1,1,name)
        productname.append(name)
    print u"中间什么也没？"
    for q in range(1,nrows):#取第一行的数
        pro_name=productname[q]
        key_one=key1[q]
        key_two=key2[q]
        key_three=key3[q]
        thread=[]
        if key_one:
            print pro_name
            thread1 = YMX(pro_name,key_one,q,5,ws,country)
            thread1.setDaemon(True)
            thread1.start()
            thread.append(thread1)
        if key_two:
            thread2 = YMX(pro_name,key_two,q,6,ws,country)
            thread2.setDaemon(True)
            thread2.start()
            thread.append(thread2)
        print key_three
        if key_three:
            print u'第三个有？'
            print key_three
            print '2222222'
            thread3 = YMX(pro_name,key_three,q,7,ws,country)
            thread3.setDaemon(True)
            thread3.start()
            thread.append(thread3)
        print len(thread)
        print "----------------------------------------"
        for th in thread:
            th.join()
    xlsNameIndex = file_name.rindex("/")
    xlsName = file_name[xlsNameIndex+1:]
    #downPath="./load/a.xls"
    print user.username
    downPath = "./load/"+user.username+xlsName
    wb.save(downPath) #修改
    endtime=time.time()
    print str(endtime-starttime)+u'秒'
    user.use_upfile_set.filter(filepath=file_name).update(fileflag=1,upload = downPath)
    print "over"

    #通知下载好，显示可下载按钮
    # print 'over'
    # f = open(file_name)
    # data = f.read()
    # f.close()
    # print 'qqqqqq'
    # response = HttpResponse(data,mimetype='application/octet-stream')
    # response['Content-Disposition'] = 'attachment; filename=%s' % file_name
    # return response




