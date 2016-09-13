#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# © 2009-2016 ZHAN.com All Rights Reserved.
# @file        : OpManage/urls.py
# @author      : Li90.COM
# @revision    : 2016-08-1 18:44:51
# @brief       :
from django.conf.urls import patterns, include, url
#from Api import urls as Api_urls
#from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework import routers
#from Api.views import *

from django.contrib import admin
admin.autodiscover()

#router=routers.DefaultRouter()
#router.register('user',UserViewSet)
#router.register('group',GroupViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OpManage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^api/auth/',include(router.urls)),
    url(r'^api/v1/',include('Api.urls')), #settings中注册app后使用单引号不需要import
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
)

