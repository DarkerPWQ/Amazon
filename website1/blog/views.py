
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render,HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader,Context
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse
from blog.models import Loginuser,User111
import os
import datetime
import httplib2
from django.template import RequestContext
#from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from blog.models import *#系统用户表
import time
import threading
import urllib2
import re
import requests
from lxml import etree
import json
from forms import *
# from django.contrib.auth.views import logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,login
from django.contrib import auth
import random
from blog.tasks import add,dealxls,add111
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class LoginForm(forms.Form):
    email=forms.CharField(label='emai',max_length=100)
    #这里的label是表头的名字,widget设置密码的密文。
    pwd=forms.CharField(label='pwd',widget=forms.Textarea())

class UserForm(forms.Form):
    # username11 = forms.CharField()
    headImg = forms.FileField()
def pwq(request):
    print "in"
    print "-----------"
    time.sleep(5)
    return render_to_response('pwq.html',{'title':u'秘密的网页','pwq':u"宫婉婷I love you"})



@login_required
def big(request):

    username = request.user.username
    print username
    t=loader.get_template('big.html')
    c=Context({"name":'pwq'})
    return HttpResponse(t.render(c))

def index1(request):
    username = request.user.username
    Usernameobj = Loginuser.objects.get(username = username)
    #创建Queryproducts，通过Username
    allProductdb=Usernameobj.display_set.all()#得到该用户所有展示商品
    #将数据库内容显示为列表
    posts_list=[]
    for everyProduct in allProductdb:
        everyProductlist={}
        everyProductlist['Asin']=everyProduct.Asin
        everyProductlist["productname"] = everyProduct.productname
        everyProductlist["productkeyword1"] = everyProduct.productkeyword1
        everyProductlist["productkeyword2"] = everyProduct.productkeyword2
        everyProductlist["productkeyword3"] = everyProduct.productkeyword3
        posts_list.append(everyProductlist)
    #现在的post_list存放的是需要显示的数据

    page_size=2
    paginator = Paginator(posts_list, page_size)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
        print page
    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    t = loader.get_template("html.html")
    c = Context({ 'posts' : posts })
    return HttpResponse(t.render(c))
def text1(request):
    print "good"
    json_list = [10, 52, 200, 334, 390, 330, 220]
    # json_dict = [
    #             {'value':335, 'name':'直接访问'},
    #             {'value':210, 'name':'有奖'},
    #             {'value':335, 'name':'直接访问'},
    #             {'value':335, 'name':'直接访问'},
    #             {'value':335, 'name':'直接访问'}]
    a = [['周一','周二','周三','周四','周五','周六','周日'],[11, 11, 15, 13, 12, 13, 10],[1, -2, 2, 5, 3, 2, 0]]
    return HttpResponse(json.dumps(a))
def text(request):
    print "jaja"
    json_list = [10, 52, 200, 334, 390, 330, 220]
    return render_to_response('dem.html')

def foo(request,p1):
    t=loader.get_template('html1')
    c=Context({"title":"濮文强","time":datetime.now(),'pwq':p1})
    return HttpResponse(t.render(c))
def TestResult(result):
    print "22222222222"
    #if 'height' and 'width' and 'Amazon' in result:
    if 'height' in result or 'Amazon ' in result:
        print "11"
        return False
    print "22"
    return True
#通过asin找出商品名称
def getProductName(request,asin,country):
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
        h = httplib2.Http(".cache")
        resp, content = h.request(url,headers=headers)
        # if  country =="es":
        #     pattern = re.compile('<title>(.*?): ',re.S)
        #     result = re.findall(pattern,content)
        #     i=result[0].strip()
        #     i=i.replace("&#39;","'").replace("&amp;quot;",'"').replace("&quot;",'"').replace("&amp;","&")
        #     result=TestResult(i)
        #     if result:
        #         return i
        #     return False
        # if  country =="de":
        #     pattern = re.compile('<span id="productTitle" class="a-size-large">(.*?)</span>',re.S)
        #     result = re.findall(pattern,content)
        #     i=result[0].strip()
        #     result=TestResult(i)
        #     if result:
        #         return i
        #     return False

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
def getAllInfo(request,Result):
    print 'jin'
    temp_dict_child = {}
    temp_dict_child2 = {}
    temp_dict_child3 = {}
    allList = []
    temp_dict_child["productkeyword"] = Result.productkeyword1
    temp_dict_child["productrank"] = Result.productrank1
    temp_dict_child["productindex"] = Result.productindex1
    temp_dict_child["varyindex"] = Result.varyindex1
    temp_dict_child["pic"] = Result.pic1
    allList.append(temp_dict_child)
    temp_dict_child2["productkeyword"] = Result.productkeyword2
    temp_dict_child2["productrank"] = Result.productrank2
    temp_dict_child2["productindex"] = Result.productindex2
    temp_dict_child2["varyindex"] = Result.varyindex2
    temp_dict_child2["pic"] = Result.pic2
    allList.append(temp_dict_child2)
    temp_dict_child3["productkeyword"] = Result.productkeyword3
    temp_dict_child3["productrank"] = Result.productrank3
    temp_dict_child3["productindex"] = Result.productindex3
    temp_dict_child3["varyindex"] = Result.varyindex3
    temp_dict_child3["pic"] = Result.pic3
    allList.append(temp_dict_child3)
    return allList
def ajaxResult(request):#重要部分
    print u"进来没啊"
    mylock = threading.RLock()
    class YMX(threading.Thread):
        def __init__(self,key,goods,num,country):#写反了，但不改了
            print u'第'+str(num)
            threading.Thread.__init__(self)
            self.basegood = unicode(goods)
            print "22222"
            self.basegood1 = '&keywords='+unicode(goods)
            # self.key = key.strip()
            print "22222111111111"
            # try:
            #     self.key = key.decode('gbk')#非常非常重要
            # except:
            #     self.key =key
            #self.key = key.decode('gbk')#非常非常重要、
            self.key =key
            self.country = country
            self.success=0
            self.num = num
            self.a=""
            self.rank=0
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
                #content=selector.xpath('//h2[@class="a-size-medium a-color-null s-inline  s-access-title  a-text-normal"]/text()')
                result=[]
                for item in range(self.items,self.items+20):
                    string = '//li[@id="result_'+str(item)+'"]/div/div/div/div[2]/div[2]/a/h2/text()'
                    #print string
                    content=selector.xpath(string)
                    if(content):
                        print "h"
                        result.append(content[0])
                self.items=self.items+len(result)
                print u'现在的'+str(self.items)

                # if(len(result)==0):
                #     h = httplib2.Http()
                #     resp, page = h.request(url,headers=headers)
                #     selector=etree.HTML(page)
                #     #content=selector.xpath('//h2[@class="a-size-medium a-color-null s-inline  s-access-title  a-text-normal"]/text()')
                #     result=[]
                #     for item in range(20):
                #         string = '//li[@id="result_'+str(item)+'"]/div/div/div/div[2]/div[2]/a/h2/text()'
                #         #print string
                #         content=selector.xpath(string)
                #         if(content):
                #             result.append(content[0])
                #self.rank=self.ranklen(content)
                #print str(len(content))+u'个'
                #self.rank=0
                n = 0#真正商品的计数

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
                # self.rank=self.rank-2
            except urllib2.URLError, e:
                if hasattr(e,"reason"):
                    print u"连接亚马逊失败,错误原因",e.reason
                    #return None
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
                if not self.success:#如果没成功，再试一次、
                    print u"没成功再来一次试试"
                    n = self.getPage(url)
                if self.success:
                    mylock.acquire()
                    Result=Queryproducts.objects.get(loginuser_id=Usernameobj.id,productname = self.key,querytime=nowtime_char,country = self.country)
                    self.a = u'在第'+str(i)+u'页的第'+ str(n) +u'个'
                    print self.a
                    if self.num==1:
                        Result.productrank1=self.a
                        Result.productindex1=self.rank
                        Result.flag1 = 1

                    elif self.num==2:
                        Result.productrank2=self.a
                        Result.productindex2=self.rank
                        Result.flag2 = 1
                    else:
                        Result.productrank3=self.a
                        Result.productindex3=self.rank
                        Result.flag3 = 1
                    Result.save()
                    mylock.release()
                    break
            if not self.success:
                mylock.acquire()
                Result=Queryproducts.objects.get(loginuser_id=Usernameobj.id,productname = self.key,querytime=nowtime_char,country = self.country)
                self.a = u'在六页以后'
                print self.a
                if self.num==1:
                    Result.productrank1=self.a
                    Result.productindex1=">100"
                    Result.flag1 = 1
                elif self.num==2:
                    Result.productrank2=self.a
                    Result.productindex2=">100"
                    Result.flag2 = 1
                else:
                    Result.productrank3=self.a
                    Result.productindex3=">100"
                    Result.flag3 = 1
                Result.save()
                mylock.release()
        def run(self):
            print 'MyThread1 starting','at:',time.ctime()
            self.res = apply(self.deal)
            print 'finish at:',time.ctime()
    username = request.user.username
    print username
    Usernameobj = Loginuser.objects.get(username = username)
    #创建Queryproducts，通过Username
    alldisplaygoods=Usernameobj.display_set.all() #得到该用户所有展示商品
    productobj=[]
    q=str(datetime.datetime.now())[0:10]
    nowtime = datetime.datetime.strptime(q, "%Y-%m-%d")
    nowtime_char=str(nowtime)[0:10]#当前时间的字符串
    aftertime = nowtime - datetime.timedelta(days = 1)#获取昨天的时间
    aftertime_char=str(aftertime)[0:10]#昨天时间的字符串
    print aftertime_char
    for one_display in alldisplaygoods:#所有展示的数据库的单个obj。
        temp_dict = {}
        temp_dict["child"]=[]
        temp_dict["id"] = one_display.id
        temp_dict["Asin"] = one_display.Asin
        temp_dict["country"] = one_display.countryname
        Asin = one_display.Asin
        temp_dict["productname"] = one_display.productname
        # print "-------------------"
        # print one_display.productname
        temp_dict["productkeyword1"] = one_display.productkeyword1
        temp_dict["productkeyword2"] = one_display.productkeyword2
        temp_dict["productkeyword3"] = one_display.productkeyword3
        #这里的one_display是每个商品的对象
        Result=Queryproducts.objects.filter(loginuser_id=Usernameobj.id).filter(productname = one_display.productname).filter(querytime = nowtime_char).filter(Asin =Asin).filter(country=one_display.country)
        if Result:#如果数据库里面有今天的数据，直接取(新增，对关键词的标志位进行查询，是否有新添的关键词（flag）)
            print u'有数据了'
            thread_list=[]#及时查询模块
            if Result[0].productkeyword1 and Result[0].flag1!=1:#有关键词但是没有查询。
                thread1 = YMX(one_display.productname,Result[0].productkeyword1,1,Result[0].country)
                thread1.setDaemon(True)
                thread1.start()
                thread_list.append(thread1)
            if Result[0].productkeyword2 and Result[0].flag2!=1:#有关键词但是没有查询。
                thread2 = YMX(one_display.productname,Result[0].productkeyword2,2,Result[0].country)
                thread2.setDaemon(True)
                thread2.start()
                thread_list.append(thread2)
            if Result[0].productkeyword3 and Result[0].flag3!=1:#有关键词但是没有查询。
                thread3 = YMX(one_display.productname,Result[0].productkeyword3,3,Result[0].country)
                thread3.setDaemon(True)
                thread3.start()
                thread_list.append(thread3)
            for thread in thread_list:
                thread.join()
            print '222222222222222222222222222222222222222'
            Result=Queryproducts.objects.filter(loginuser_id=Usernameobj.id).filter(productname = one_display.productname).filter(querytime = nowtime_char).filter(Asin =Asin).filter(country=one_display.country)
            #print Result
            temp_dict["child"] = getAllInfo(request,Result[0])
            print temp_dict["child"]
            # temp_dict_child["productkeyword"] = Result[0].productkeyword1
            # temp_dict_child["productrank"] = Result[0].productrank1
            # temp_dict_child["productindex"] = Result[0].productindex1
            # temp_dict_child["varyindex"] = Result[0].varyindex1
            # temp_dict_child["varyindex"] = Result[0].varyindex1
            # temp_dict_child["pic"] = Result[0].pic1
            # temp_dict["child"].append(temp_dict_child)
            # temp_dict_child2["productkeyword"] = Result[0].productkeyword2
            # temp_dict_child2["productrank"] = Result[0].productrank2
            # temp_dict_child2["productindex"] = Result[0].productindex2
            # temp_dict_child2["varyindex"] = Result[0].varyindex2
            # temp_dict_child2["varyindex"] = Result[0].varyindex2
            # temp_dict_child2["pic"] = Result[0].pic2
            # temp_dict["child"].append(temp_dict_child2)
            # temp_dict_child3["productkeyword"] = Result[0].productkeyword3
            # temp_dict_child3["productrank"] = Result[0].productrank3
            # temp_dict_child3["productindex"] = Result[0].productindex3
            # temp_dict_child3["varyindex"] = Result[0].varyindex3
            # temp_dict_child3["varyindex"] = Result[0].varyindex3
            # temp_dict_child3["pic"] = Result[0].pic3
            # temp_dict["child"].append(temp_dict_child3)
            productobj.append(temp_dict)#是完整的了
        else:#今天的数据不存在
            afterdata=Queryproducts.objects.filter(loginuser_id=Usernameobj.id).filter(productname = one_display.productname).filter(querytime = aftertime_char).filter(Asin =Asin).filter(country=one_display.country)
            if afterdata:#昨天有数据,今天没数据，爬（但是按照现在数据的关键词等，所以不能从昨天的数据抽取关键字）
                print u' 昨天有数据,今天没数据'
                #one_display.productname#今天数据的的名字，应该先在Q创建好该商品，为了待会多线程方便
                Queryproducts.objects.create(Asin =one_display.Asin,productname = one_display.productname,productkeyword1=one_display.productkeyword1,
                                             productkeyword2=one_display.productkeyword2,productkeyword3=one_display.productkeyword3,loginuser_id=Usernameobj.id,querytime = nowtime_char,country = one_display.country,countryname = one_display.countryname)
                keyword=[]
                index_l=[]
                if one_display.productkeyword1:
                    index_l.append(1)
                    keyword.append(one_display.productkeyword1)
                if one_display.productkeyword2:
                    keyword.append(one_display.productkeyword2)
                    index_l.append(2)
                if one_display.productkeyword3:
                    keyword.append(one_display.productkeyword3)
                    index_l.append(3)
                thread_list=[]
                for i in keyword:
                    a = index_l[keyword.index(i)]
                    print a
                    thread1 = YMX(one_display.productname,i,a,one_display.country)
                    thread1.setDaemon(True)
                    thread1.start()
                    thread_list.append(thread1)
                for thread in thread_list:
                    thread.join()
                print "here"
                afterindex1=afterdata[0].productindex1#修改之后的数据类型是字符串，如果需要计算需要转化数据类型。
                afterindex2=afterdata[0].productindex2
                afterindex3=afterdata[0].productindex3
                now_obj=Queryproducts.objects.get(loginuser_id=Usernameobj.id,productname = one_display.productname,querytime = nowtime_char,Asin=one_display.Asin,country = one_display.country)
                #由于django不能设置默认值，减法在没有值得情况下会报错，所以现在判断对应前关键字是否存在。
                print u'设置开始计算趋势'
                # if now_obj.productkeyword1 and now_obj.productkeyword1!=">100":#查看现在是否由关键字1
                if now_obj.productkeyword1:
                    if now_obj.productindex1!=">100":
                        if afterdata[0].productkeyword1 and afterdata[0].productindex1!=">100":#是否昨天由关键字
                            try:
                                varyindex1=int(afterindex1)-int(now_obj.productindex1)
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
                                print '1'
                            except:
                                pass
                        else:
                            now_obj.varyindex1=u'新进入排名区'
                            now_obj.pic1 = 'wu'

                    else:
                        print u"来了呀"
                        now_obj.varyindex1=u'未进入排名区'
                        now_obj.pic1 = 'wu'

                    # if afterdata[0].productindex1 and now_obj.productkeyword1!=">100":#是否昨天由关键字
                    #     try:
                    #         varyindex1=int(afterindex1)-int(now_obj.productindex1)
                    #         if varyindex1>0:
                    #             pic1='up'
                    #         elif varyindex1==0:
                    #             pic1='wu'
                    #         else:
                    #             pic1='down'
                    #         now_obj.varyindex1=varyindex1
                    #         now_obj.pic1=pic1
                    #         print '1'
                    #     except:
                    #         pass
                    # else:#现在刚加的关键字
                    #     now_obj.varyindex1=u'新增词'
                    #     now_obj.pic1 = 'wu'
                if now_obj.productkeyword2:
                    if now_obj.productindex2!=">100":
                        if afterdata[0].productkeyword2 and afterdata[0].productindex2!=">100":#是否昨天由关键字
                            try:
                                varyindex2=int(afterindex2)-int(now_obj.productindex2)
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
                                print '1'
                            except:
                                pass
                        else:
                            now_obj.varyindex2=u'新进入排名区'
                            now_obj.pic2 = 'wu'

                    else:
                        now_obj.varyindex2=u'未进入排名区'
                        now_obj.pic2 = 'wu'
                if now_obj.productkeyword3:
                    if now_obj.productindex3!=">100":
                        if afterdata[0].productkeyword3 and afterdata[0].productindex3!=">100":#是否昨天由关键字
                            try:
                                varyindex3=int(afterindex3)-int(now_obj.productindex3)
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
                                print '1'
                            except:
                                pass
                        else:
                            now_obj.varyindex3=u'新进入排名区'
                            now_obj.pic3 = 'wu'
                    else:
                        now_obj.varyindex3=u'未进入排名区'
                        now_obj.pic3 = 'wu'
                now_obj.save()
                temp_dict["child"] = getAllInfo(request,now_obj)

                productobj.append(temp_dict)
            else:#昨天也没数据,所以变化指数和图片都可以放入平直。
                print u'昨天也没数据'
                Queryproducts.objects.create(Asin=one_display.Asin,productname = one_display.productname,productkeyword1=one_display.productkeyword1,
                                             productkeyword2=one_display.productkeyword2,productkeyword3=one_display.productkeyword3,loginuser_id=Usernameobj.id,querytime = nowtime_char,country=one_display.country,countryname = one_display.countryname)
                keyword=[]
                index_l=[]
                if one_display.productkeyword1:
                    index_l.append(1)
                    keyword.append(one_display.productkeyword1)
                if one_display.productkeyword2:
                    keyword.append(one_display.productkeyword2)
                    index_l.append(2)
                if one_display.productkeyword3:
                    keyword.append(one_display.productkeyword3)
                    index_l.append(3)
                #print keyword
                thread_list=[]
                print "??"
                for i in keyword:
                    a = index_l[keyword.index(i)]
                    thread1 = YMX(one_display.productname,i,a,one_display.country)
                    thread1.setDaemon(True)
                    thread1.start()
                    thread_list.append(thread1)
                for thread in thread_list:
                    thread.join()
                #数据已爬完，进一步处理所以变化指数和图片都可以放入平直。

                now_obj=Queryproducts.objects.get(loginuser_id=Usernameobj.id,productname = one_display.productname,querytime = nowtime_char,country =one_display.country)
                print now_obj
                print u'到了这一步了，出现了问题'
                now_obj.pic1='wu'
                now_obj.pic2='wu'
                now_obj.pic3='wu'
                now_obj.save()
                now_obj.varyindex1=u'新增'
                now_obj.varyindex2=u'新增'
                now_obj.varyindex3=u'新增'
                now_obj.save()
                print u'到了这一步了，出现了问题数据类型改写错误'
                print 'lai '
                temp_dict["child"] = getAllInfo(request,now_obj)
                productobj.append(temp_dict)
        print "for"
        #productobj.append(temp_dict)
        #print productobj
        #为了采用ajax不刷新网页，所以要把现在的东西给传回去，而不能刷新网页
        #思考能不能传回去个数据库？不回去，那么现在方法吧对应的数据库里面的东西都读出来放到list中去。
    print 'wwww'
    dict = {'productobj':productobj}
    return HttpResponse(json.dumps(dict))
def del_pro(request):#删除操作
    #product_id = request.POST.get('product_id')
    username = request.user.username
    print u'还是可以得到用户名11'
    print username
    if request.method == 'POST':
        req = json.loads(request.body)
        print req
        product_id = req['product_id']#display中的产品id.
        print product_id
        #数据库大小写的由来与依靠，还有就是print导致数据库的停止！
        productobj = Display.objects.get(id=int(product_id))#出现问题，找不

        productobj.delete()

        Usernameobj = Loginuser.objects.get(username = username)
        #alldisplaygoods=Usernameobj.display_set.all() #采用小写
        alldisplaygoods = Display.objects.filter(loginuser_id=Usernameobj.id)
        productobj=[]
        for one_display in alldisplaygoods:
            print "for"
           # Usernameobj.Queryproducts_set.create(productname = 'hbyuh')
            print '111'
            temp_dict = {}
            temp_dict["id"] = one_display.id
            temp_dict["Asin"] = one_display.Asin
            temp_dict["country"] = one_display.countryname
            temp_dict["productname"] = one_display.productname
            temp_dict["productkeyword1"] = one_display.productkeyword1
            temp_dict["productkeyword2"] = one_display.productkeyword2
            temp_dict["productkeyword3"] = one_display.productkeyword3
            productobj.append(temp_dict)

        #为了采用ajax不刷新网页，所以要把现在的东西给传回去，而不能刷新网页
        #思考能不能传回去个数据库？不回去，那么现在方法吧对应的数据库里面的东西都读出来放到list中去。
    print 'wwww'
    dict = {'productobj':productobj}
    #dict = {'display_id':dispaly_id,'productobj':productobj }
    print 'stop'
    #return HttpResponse(json.dumps(dict), content_type='application/json')
    return HttpResponse(json.dumps(dict))
import json
def addDefined(request):#增加自定义查询时，对query的添加
    #product_id = request.POST.get('product_id')
    username = request.user.username
    print u'还是可以得到用户名'
    print username
    q=str(datetime.datetime.now())[0:10]
    nowtime = datetime.datetime.strptime(q, "%Y-%m-%d")
    nowtime_char=str(nowtime)[0:10]#当前时间的字符串
    Usernameobj = Loginuser.objects.get(username = username)
    if request.method == 'POST':
        req = json.loads(request.body)
        product_id = req['product_id']#display中的产品id.
        addword = req['addword']#用户自定义的关键词,
        #接下来就是把该关键词添加到display中。
        print product_id

        productobj = Display.objects.get(id=int(product_id))#不需要在[[0]
        print "22222222"
        productName = productobj.productname
        #print productName
        print nowtime_char
        queryproduct = Usernameobj.queryproducts_set.filter(productname = productName,querytime = nowtime_char)#有问题
    
        keylist=[]
        if productobj.productkeyword1:
            keylist.append(productobj.productkeyword1)
        if productobj.productkeyword2:
            keylist.append(productobj.productkeyword2)
        if productobj.productkeyword3:
            keylist.append(productobj.productkeyword3)
        keyname=len(keylist)
        if keyname==3:
            error=u"关键词已有三个"
            dict = {'error':'have','content':error}
            #return HttpResponse(json.dumps(dict), content_type='application/json')
            return HttpResponse(json.dumps(dict))
        print "222222222222222"
        if not productobj.productkeyword1:
           productobj.productkeyword1 = addword#更新
           if queryproduct:
               queryproduct[0].productkeyword1 = addword
        elif not productobj.productkeyword2:
            productobj.productkeyword2 = addword#更新
            if queryproduct:
                queryproduct[0].productkeyword2 = addword
        elif not productobj.productkeyword3:
            productobj.productkeyword3 = addword#更新
            if queryproduct:
                print "eeeeeee"
                queryproduct[0].productkeyword3 = addword
        productobj.save()
        if queryproduct:
            queryproduct[0].save()#youwenti
        productobj=[]
        Usernameobj = Loginuser.objects.get(username = username)
        print Usernameobj.id
        alldisplaygoods=Usernameobj.display_set.all() #采用小写
        #alldisplaygoods = Display.objects.filter(loginuser_id=Usernameobj.id)
        for one_display in alldisplaygoods:
            temp_dict = {}
            temp_dict["id"] = one_display.id
            temp_dict["Asin"] = one_display.Asin
            temp_dict["country"] = one_display.countryname
            temp_dict["productname"] = one_display.productname
            temp_dict["productkeyword1"] = one_display.productkeyword1
            temp_dict["productkeyword2"] = one_display.productkeyword2
            temp_dict["productkeyword3"] = one_display.productkeyword3
            productobj.append(temp_dict)

        #为了采用ajax不刷新网页，所以要把现在的东西给传回去，而不能刷新网页
        #思考能不能传回去个数据库？不回去，那么现在方法吧对应的数据库里面的东西都读出来放到list中去。


    dict = {'username1':product_id,'productobj':productobj ,'error':''}
    print 'stop'

    #return HttpResponse(json.dumps(dict), content_type='application/json')
    return HttpResponse(json.dumps(dict))
    # product_id = json.shoads(product_id)

def demo(request):
    return render_to_response('demo.html')
def ajax_list(request):
    a = range(100)
    return HttpResponse(json.dumps(a), content_type='application/json')
    #不加json的话不能正确的输出list，type更好地输出格式。
def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')

def ajax_deal(request):
    print '2222222'
    return HttpResponse("hello")
# def add(request):
#     a = request.GET['a']
#     b = request.GET['b']
#     a = int(a)
#     b = int(b)

    # return HttpResponse(str(a+b))
    #return HttpResponse('sssssss')
# def index1(request):
#     return render_to_response('index1.html')
@login_required
def up(request):
    crawlflag = 0
    username = request.user.username
    print username
    if 'up' in request.POST:
    # if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            a=request.FILES['headImg']#这里的a就是文件了
            file_name=dealup(request,a)#得到文件准确地址
            middleuser = Loginuser.objects.filter(username = username)#通过用户名找到数据对象，注意是set
            print type(middleuser)
            middleuser[0].use_upfile_set.create(filepath=file_name,fileflag=0)#通过外键来创建
            dealxls.delay(file_name,middleuser[0])#后端异步处理中：入口参数文件准确地址和用户

            # dealxls(request,file_name)
            # username = uf.cleaned_data['username11']
            # headImg = uf.cleaned_data['headImg']
            #写入数据库，与此同时也存进了数据库规定的位置中，，但是其实我们是想让每个用户都分类，所以我们想自己处理
            # user = User111()
            # user.username = username
            # user.headImg = headImg
            # user.save()
            return HttpResponse('upload ok111!')
            return render_to_response('up.html',{'uf':uf,'crawlflag':crawlflag})
    elif 'up11' in request.POST:
        print request.POST
        print 'here'
        return HttpResponse('upload ok111!')
    else:
        uf = UserForm()
    middleuser = Loginuser.objects.filter(username = username)
    obj = use_upfile.objects.filter(loginuser_id =middleuser[0].id)#如何通过外键去找到对象
    print '11'
    if obj:
        #处理多个任务
        numup = len(obj)
        print u"有"+str(numup)+u"个上传任务" #同时上传多个任务的时候怎么分辨呢
        for i in obj:
            if i.fileflag:
                crawlflag =i.fileflag
                break
        print 'jinlai '
        # realpath = down_url[1:]
        # print realpath
    print crawlflag #当初这里遇到了就是0在前端也显示，因为数据库里面这个字段之字符型，不是数值型，就算是0也被认为是True
    print '??'
    return render_to_response('up.html',{'uf':uf,'crawlflag':crawlflag})
    # return render_to_response('up.html',{'uf':uf,'uf1':uf1})
def dealup(request,f):
    username = request.user.username
    print username
    print f.name #获取文件名
    try:
        print u'Jin来'
        uploadname = f.name
        path = "./upload/" +username+ time.strftime('/%Y/%m/%d/%H/')#按时间划分文件夹的方法
        if not os.path.exists(path):#创建该文件
            os.makedirs(path)
            file_name = path + f.name
            print file_name#最终的位置
        else:
            file_name = path + f.name
        destination = open(file_name, 'wb+') #保存文件，以用来其他操作，
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        print u'保存成功'
    except Exception, e:
        print e
    return file_name

def download1(request):#结果文件下载，
    username = request.user.username#获取用户
    print username
    import mimetypes
    print '11qq'
    middleuser = Loginuser.objects.filter(username = username)
    obj = use_upfile.objects.filter(loginuser_id =middleuser[0].id).filter(fileflag=1)
    if not obj:
        return HttpResponse('no!')
    # file_path=obj[0].filepath#如何通过外键去找到对象，相应的id
    file_path=obj[0].upload
    def file_iterator(file_path, chunk_size=512):
        with open(file_path,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    print file_path
    print "download"


    # response = HttpResponse(file_iterator(file_path),content_type='application/octet-stream')
    # response['Content-Disposition'] = 'attachment; filename=%s' % file_path
    obj[0].delete()#删除该对象，下载完成
    # response = HttpResponse(file_iterator(file_path))
    #
    # return response
    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_path)
    return response
def download(request):#模板文件的下载
    print "模板"
    username = request.user.username#获取用户
    down_url="./static/keywordmonitor.xls"
    f = open(down_url,'rb')#这里打开方式一定要是rb！！！
    data = f.read()
    f.close()
    response = HttpResponse(data,content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % down_url
    return response

def regist(request):
    print u"进来注册了"
    if request.method == 'POST':
        print u"进来注册了"
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        email = request.POST.get('email',None)
        print username
        print password
        print email
        if username and password:
            if not Loginuser.objects.filter(username=username):
                add.delay()#异步任务执行
                #Celery会将task加入到queue中, 并马上返回. 而在一旁待命的worker看到该task后, 便会按照设定执行它, 并将他从queue中移除.

                # a=Loginuser(username= username,password=password,email=email)
                Loginuser.objects.create(username= username,password=password,email=email)
                user = User.objects.create_user(username= username,password=password,email=email)
                user.save()
                return HttpResponseRedirect('/accounts/login/')
            else:
                error = '该用户名已被注册，请重新选择一个用户名'
                return render_to_response('regist.html',{'error':error})
                #return HttpResponse('该用户名已被注册，请重新选择一个用户名')
        else:
            error = '用户名或密码不能为空'
            return render_to_response('regist.html',{'error':error})

    return render_to_response('regist.html',{})
@login_required
def home(request):
    crawlflag = 0
    username = request.user.username
    print username
    print request.POST
    if 'up' in request.POST:#上传部分
        country=request.POST.get('countryup',None)#获取国家
        countryname = getCountryName(request,country)
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            a=request.FILES['headImg']#这里的a就是文件了
            file_name=dealup(request,a)#得到文件准确地址
            Username = Loginuser.objects.filter(username = username)#通过用户名找到数据对象，注意是set
            print type(Username)
            Username[0].use_upfile_set.create(filepath=file_name,fileflag=0)#通过外键来创建
            dealxls.delay(file_name,Username[0],country)#后端异步处理中：
            #读到页面上去
            print u'进来？？'
            from xlrd import open_workbook
            wb1 = open_workbook(unicode(file_name))
            for s in wb1.sheets():
                if s.nrows:#获取行数
                    nrows = s.nrows
                    print nrows
                else:
                    break#不出来空循环！！
                for i in range(1,nrows):
                    print '77'
                    data=s.row_values(i)#这个总是出错，原因不能超过表的范围
                    #一开始以为会由于长度问题，其实不会。因为空白被读出来了！
                    productname = getProductName(request,data[0],country)
                    if productname:
                        if not Username[0].display_set.all().filter(productname = productname,Asin = data[0],country = country):
                            Username[0].display_set.create(Asin = data[0],productname = productname,productkeyword1=data[2],
                                                               productkeyword2=data[3],productkeyword3=data[4],country = country,countryname=countryname)#通过外键来创建
            print u'创建成果'
            return render_to_response('home.html',{'username':username,'uf':uf,'crawlflag1':crawlflag,'display':Username[0],})
            #return HttpResponse('upload ok111!')
            #return render_to_response('up.html',{'uf':uf,'crawlflag':crawlflag})
    else:
        uf = UserForm()
        if request.method == 'POST':
            asin = request.POST.get('asin',None)#获取前端的内容
            country = request.POST.get("country",None)#获取国家站点
            print country
            print asin
            Username = Loginuser.objects.filter(username = username)
            if Display.objects.filter(loginuser_id=Username[0].id,Asin = asin,country = country):
                error = u"已有该商品的监督，请查询其他商品"
                return render_to_response('home.html',{'username':username,'uf':uf,'crawlflag1':crawlflag,'display':Username[0],'error':error})
            print "sudo"
            productname = getProductName(request,asin,country)
            #判断是否超过50个监控
            displaynum = Display.objects.filter(loginuser_id=Username[0].id).count()

            if not productname:
                error = u"查询商品为空，请重新输入"
                #只是提醒超过50，其他功能应该可以继续用
                return render_to_response('home.html',{'username':username,'uf':uf,'crawlflag1':crawlflag,'display':Username[0],'error':error})
            if displaynum > 50:
                error = u"您监控查询的产品数超过50个了，请删除后重新输入"
                #只是提醒超过50，其他功能应该可以继续用
                return render_to_response('home.html',{'username':username,'uf':uf,'crawlflag1':crawlflag,'display':Username[0],'error':error})
            else:#新增的商品
                countryName = getCountryName(request,country)
                Username[0].display_set.create(Asin=asin,productname=productname,country = country,countryname = countryName)#通过外键来创建
                return render_to_response('home.html',{'username':username,'uf':uf,'crawlflag1':crawlflag,'display':Username[0]})
           # return render_to_response('home.html',{'username':username,'uf':uf,'crawlflag1':crawlflag,'display':Username[0]})
    uf = UserForm()
    Username = Loginuser.objects.filter(username = username)
    print Username
    print "111"

    obj = use_upfile.objects.filter(loginuser_id =Username[0].id)#如何通过外键去找到对象，查看是否有下载好的文件
    print '11'
    if obj:
        #处理多个任务
        numup = len(obj)
        print u"有"+str(numup)+u"个上传任务" #同时上传多个任务的时候怎么分辨呢
        for i in obj:
            if i.fileflag:
                crawlflag =i.fileflag
                break
    return render_to_response('home.html',{'username':username,'uf':uf,'crawlflag1':crawlflag,'display':Username[0],'queryflag':1})
    #return render_to_response('home.html',{'username':username,'middleuser':middleuser,'uf':uf,'crawlflag':crawlflag,'remind':remind})
def getCountryName(request,name):#获取国家全称
    if name=="com":
        return u"美国"
    elif name=="de":
        return u"德国"
    elif name=="fr":
        return u"法国"
    elif name=="co.uk":
        return u"英国"
    elif name=="es":
        return u"西班牙"
    else:
        return u"意大利"


def Login(request):
    if request.method == 'POST':
        username=request.POST.get('username',None)
        password=request.POST.get('password',None)
        #user = Loginuser.objects.filter(email=email,password = password)
        user = Loginuser.objects.filter(username = username,password = password)
        print user
        user2 = authenticate(username=username,password = password)
        # user2 = authenticate(email=email, password=password)
        print '1'
        if user2 and user:
            if user2.is_active:
                # login(request, user2)
                login(request, user2)
                #这句才是起到关键的地方。告诉浏览器我们在登录。后续的其他一切网站都是已这个为登录的。
                #而且这个user2不是简单的账号密码了，而是对象了。
                # return HttpResponse('sucess')
                return HttpResponseRedirect('/blog/home')
            else:
                return HttpResponse("Invalid login details supplied.")
        else:
            error = '您输入的用户名或密码有错误，请重新输入'
            return render_to_response('login.html',{'error':error})
    return render_to_response('login.html')

def logout(req):
    auth.logout(req)
    return HttpResponseRedirect('/accounts/login/')
    return HttpResponse("Invalid login details supplied.")
def pageManager(request,productObjectList):

    page_size=2
    after_range_num = 5
    before_range_num = 6
    try:
        page = int(request.GET.get("page",1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(productObjectList,page_size)
    try:
        productObjectList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        productObjectList = paginator.page(1)
    print page
    if page>after_range_num:
        page_range = paginator.page_range[int(page)-after_range_num:page+before_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+before_range_num]
    return productObjectList,page_range

def manageProduct(request):
    username = request.user.username
    p = Loginuser.objects.filter(username = username)
    p = p[0]#用户对象
    q=str(datetime.datetime.now())[0:10]
    nowtime = datetime.datetime.strptime(q, "%Y-%m-%d")
    nowtime_char=str(nowtime)[0:10]#当前时间的字符串
    if 'checkbox'in request.POST:
        delCheckList=request.POST.getlist('checkbox',None)
        nowTime=request.POST.get('nowtime',None)
        #获取多个表单值。结果为list,值是商品的名称
        for delCheck in delCheckList:
            delProductQuery = p.queryproducts_set.filter(productname=delCheck,querytime=nowTime)
            print len(delProductQuery)
            delProductQuery[0].delete()
            delProductDisplay = p.display_set.filter(productname = delCheck)
            if len(delProductDisplay)>0:
                delProductDisplay[0].delete()
        #重新读取
        dayAllProList = mamageGetProductList(request,nowTime)
        latestDistinctAllObjs,page_range = pageManager(request,dayAllProList)
        return render_to_response('manageProduct.html',{'username':username,'latestDistinctAllObjs':latestDistinctAllObjs, \
                                    'the_date':nowtime_char})
    elif 'q' in request.POST:
        print "2222222"
        the_date=request.POST.get('q',None)#获取选择的时间
        print the_date
        nowtime_char = str(the_date)
        dayAllProList = mamageGetProductList(request,nowtime_char)
        latestDistinctAllObjs,page_range = pageManager(request,dayAllProList)
        return render_to_response('manageProduct.html',{'username':username,'latestDistinctAllObjs':latestDistinctAllObjs, \
                                    'the_date':nowtime_char,'page_range':page_range})
    else:
        dayAllProList = mamageGetProductList(request,nowtime_char)
        print len(dayAllProList)
        latestDistinctAllObjs,page_range = pageManager(request,dayAllProList) #调用分页
        return render_to_response('manageProduct.html',{'username':username,'latestDistinctAllObjs':latestDistinctAllObjs, \
                                    'the_date':nowtime_char,'page_range':page_range})
def mamageGetProductList(request,time):
    username = request.user.username
    p = Loginuser.objects.filter(username = username)
    p = p[0]#用户对象
    nowtimeProobjs=p.queryproducts_set.filter(loginuser_id=p.id).filter(querytime=time)#将独享转化为列表
    dayAllProList=[]
    for obj in nowtimeProobjs:
        dayEveryProList={}
        dayEveryProList['Asin'] = obj.Asin
        dayEveryProList['country'] = obj.countryname
        dayEveryProList['productname'] = obj.productname
        dayEveryProList['productkeyword1'] = obj.productkeyword1
        dayEveryProList['productrank1'] = obj.productrank1
        dayEveryProList['productindex1'] = obj.productindex1
        dayEveryProList['varyindex1'] = obj.varyindex1
        dayEveryProList['productkeyword2'] = obj.productkeyword2
        dayEveryProList['productrank2'] = obj.productrank2
        dayEveryProList['productindex2'] = obj.productindex2
        dayEveryProList['varyindex2'] = obj.varyindex2
        dayEveryProList['productkeyword3'] = obj.productkeyword3
        dayEveryProList['productrank3'] = obj.productrank3
        dayEveryProList['productindex3'] = obj.productindex3
        dayEveryProList['varyindex3'] = obj.varyindex3
        dayAllProList.append(dayEveryProList)
    return dayAllProList
