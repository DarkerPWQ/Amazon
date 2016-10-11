from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/',include('django.contrib.admindocs.urls')),
    #url(r'^admin/', include('django.contrib.admin.urls')),
    url(r'^blog/',include('blog.urls')),
                       
    url(r'^admin/',include(admin.site.urls)),
    url(r'^accounts/login/$', 'blog.views.Login'),
     url(r'^account/loggedout/$', 'blog.views.logout'),
    # url(r'^ajax_deal/$','blog.views.ajax_deal'),
    url(r'^ajax_list/$', 'blog.views.ajax_list', name='ajax-list'),
    url(r'^ajax_dict/$', 'blog.views.ajax_dict', name='ajax-dict'),
    #url(r'^del_home$', 'blog.views.del_home'),

    
                       
)
