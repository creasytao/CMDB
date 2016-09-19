#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# © 2009-2016 ZHAN.com All Rights Reserved.
# @file        : djangoproject/mywrapper.py
# @author      : Li90.COM
# @revision    : 2016-09-18 13:49:31
# @brief       :
from functools import wraps
from django.http import HttpResponseRedirect
import views
#def _auth(args):
#    def __auth(func):
#        def _login(request):
#            username = request.user.username
#            if not username:
#                print "没登陆"
#                return views.login(request)
#            #print request.user.groups.values_list('name',flat=True)
#            for g in request.user.groups.all():
#                #if g.name in (args or auth()) or (g.name == 'admin'):
#                if g.name in args:
#                    return func(request)
#            return views.logout(request)
#        return _login
#    return __auth
def _auth(func=None, group=None, redirect=None):
    def __auth(func):
        @wraps(func)
        def _login(request, *args, **kwargs):
            username = request.user.username
            if not username:
                print "没登陆"
                return views.login(request, *args, **kwargs)
            #print request.user.groups.values_list('name',flat=True)

            for g in request.user.groups.all():
                if g.name in group:
                    if redirect:
                        return HttpResponseRedirect(redirect)
                    return func(request, *args, **kwargs)
            #    if g.name == 'admin':
            #        return func(request, *args, **kwargs)
            return views.logout(request, *args, **kwargs)

        return _login

    if not func:
        def foo(func):
            return __auth(func)
        return foo

    return __auth
