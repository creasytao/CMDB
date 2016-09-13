#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# © 2009-2016 ZHAN.com All Rights Reserved.
# @file        : Api/urls.py
# @author      : Li90.COM
# @revision    : 2016-08-2 10:09:44
# @brief       :
from django.conf.urls import patterns, include, url
from rest_framework import routers
#from rest_framework.urlpatterns import format_suffix_patterns
from Api.views import *

router=routers.DefaultRouter()
router.register('users',UserViewSet)
router.register('groups',GroupViewSet)
router.register('snippets',SnippetViewSet)

#router.register('snippets',snippet_list,'id')

urlpatterns=patterns('',
                    url(r'^',include(router.urls)),

)
#urlpatterns = format_suffix_patterns(urlpatterns)
# API endpoints
#urlpatterns = format_suffix_patterns([
#    url(r'^$', api_root),
#    url(r'^snippets/$',
#        SnippetList.as_view(),
#        name='snippet-list'),
#    url(r'^snippets/(?P<pk>[0-9]+)/$',
#        SnippetDetail.as_view(),
#        name='snippet-detail'),
#    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
#        SnippetHighlight.as_view(),
#        name='snippet-highlight'),
#    url(r'^users/$',
#        UserList.as_view(),
#        name='user-list'),
#    url(r'^users/(?P<pk>[0-9]+)/$',
#        UserDetail.as_view(),
#        name='user-detail')
#])
