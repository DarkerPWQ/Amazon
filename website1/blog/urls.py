from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('blog.views',
    # Examples:
    # url(r'^$', 'website1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^index/$','index'),
    url(r'^foo/(.*?)/$','foo'),

    #
    # #url(r'foo/(?P<id>\d{4}))/(?P<name>\w+)/$,'foo'
    # url(r'^student_list/$','student_list'),
    #url(r'^teacher/$','teacher'),
    # url(r'^login/$','login'),
    #url(r'^small/$','small'),
    #url(r'^big/$','big'),
    # url(r'^login1/$','login1'),
    url(r'^regist/$','regist'),
    url(r'^up/$','up'),
    url(r'^pwq/$','pwq'),
    url(r'^addDefined/$','addDefined'),
    url(r'^del_pro/$','del_pro'),
    url(r'^home/$','home'),
    url(r'^download/$','download'),
    url(r'^download1/$','download1'),
     url(r'^ajax_deal/$','ajax_deal'),
     url(r'^manageProduct/$', 'manageProduct'),
     url(r'^add/$','add'),
     url(r'^index1/$','index1'),
     #url(r'^demo/$','demo'),
     url(r'^ajaxResult/$','ajaxResult'),
    url(r'^text/$','text'),
    url(r'^text1/$','text1'),
                       
                       
)
