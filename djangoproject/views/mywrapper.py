#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# © 2009-2016 ZHAN.com All Rights Reserved.
# @file        : djangoproject/mywrapper.py
# @author      : Li90.COM
# @revision    : 2016-09-18 13:49:31
# @brief       :
from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
logger = logging.getLogger('sourceDns.webdns.views')
import views
#from views import *

def _auth(func=None, group=None, redirect=None, viewfunc=None):
    '''
    用法
    1、@_auth()
        验证登录通过:   则用被装饰的view返回
                        否则返回login视图
    2、@_auth(group='xxx')
        验证组权限符合: 则用被装饰的view返回
                        否则用户没有指定可用组权限并重新登录
    3、@_auth(group='xxx',redirect='yyy')
        验证组权限符合: 则跳转uri到yyy
                        否则用户没有指定可用权限组并重新登录
    4、@_auth(group='xxx',viewfunc='zzz')
        验证组权限符合: 则用zzz视图返回
                        否则用户没有指定可用权限组并重新登录
    5、特殊地，多个group验证时，请使用list类型
     e. g.  @_auth(group=['aaa','bbb','ccc'])
    '''
    def __auth(func):
        @wraps(func)
        def _login(request, *args, **kwargs):
            username = request.user.username
            if not username:
                logger.warn("没有登录")
                return views.login(request, *args, **kwargs)
            elif not group:
                logger.debug("登录检查，登录用户是:       %s" % username)
                return func(request, *args, **kwargs)

            #print request.user.groups.values_list('name',flat=True)
            for g in request.user.groups.all():
                if g.name in group:
                    if not redirect and not viewfunc:
                        logger.debug("组权限检查，用户:%s,属于组:%s,要求组:%s,执行当前视图:%s"
                                     % (username, g.name, group, func))
                        return func(request, *args, **kwargs)
                    if redirect:
                        logger.debug("组权限检查，用户:%s,属于组:%s,要求组:%s,跳转uri:%s"
                                     % (username, g.name, group, redirect))
                        return HttpResponseRedirect(redirect)
                    if viewfunc:
                        logger.debug("组权限检查，用户:%s,属于组:%s,要求组:%s,返回视图:%s"
                                     % (username, g.name, group, viewfunc))
                        return eval(viewfunc)(request, *args, **kwargs)

                #if g.name == "admin":
                #    pass
                # .
                # .
                # .

                logger.debug("组权限检查，用户:%s,属于组:%s,要求组:%s,执行当前视图:%s"
                             % (username, g.name, group, func))
                return func(request, *args, **kwargs)

            logger.warn("用户:%s 没有分配合适的组权限,将禁止访问" % username)
            #return views.logout(request, *args, **kwargs)
            #return HttpResponse(status=403)
            raise PermissionDenied

        return _login
    return __auth
