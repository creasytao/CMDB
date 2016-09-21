#coding:utf-8

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group, User
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext
from django.core import serializers

from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.decorators import login_required
from mywrapper import _auth

from forms import LoginForm,ChangepwdForm

from cmdb.models import *
import os, sys, commands, json


import logging
logger = logging.getLogger('sourceDns.webdns.views')

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/login')

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response(
            'login.html',
            locals()
        )
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(
                username=username,
                password=password
            )
            if user is not None and user.is_active:
                auth.login(request, user)
		return HttpResponseRedirect('/dashboard')
            else:
                return render_to_response(
                    'login.html', RequestContext(
                        request, {
                            'form': form,
                            'password_is_wrong':True
                        }
                    )
                )
        else:
            return render_to_response(
                'login.html',
                locals()
            )

#@login_required(login_url='/')
@_auth()
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

#@login_required(login_url='/')
@_auth()
def changepwd(request):
    redirect_to=request.GET['next']
    if request.method == 'GET':
        form = ChangepwdForm()
        return render_to_response(
            'changepwd.html',
            locals()
        )
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = auth.authenticate(
                username=username,
                password=oldpassword
            )
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
		return HttpResponseRedirect(redirect_to)
            else:
                return render_to_response(
                    'changepwd.html',
                    RequestContext(
                        request, {
                            'form': form,
                            'oldpassword_is_wrong':True
                        }
                    )
                )
        else:
            return render_to_response(
                'changepwd.html',
                locals()
            )

#@login_required(login_url='/')
@_auth()
def dashboard(request):
    return render_to_response(
        'dashboard.html',
        locals()
    )

#@login_required(login_url='/')
@_auth()
def assets(request):
    return HttpResponseRedirect('/assets/hostlist')

#@login_required(login_url='/')
@_auth()
def assets_hostlist(request):
    lines=Host.objects.all().order_by("-id")
    paginator = Paginator(lines, 10)
    page = request.GET.get('page')
    #阿里云esc获取
    #EcsGet()
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response(
        'hostlist.html',
        locals()
    )

#@login_required(login_url='/')
@_auth()
def assets_topology(request):
    return render_to_response(
        'topology.html',
        locals()
    )

#@login_required(login_url='/')
@_auth()
def configure(request):
    return render_to_response(
        'configure.html',
        locals()
    )

#@login_required(login_url='/')
@_auth()
def audit(request):
    return render_to_response(
        'audit.html',
        locals()
    )


#@login_required(login_url='/')
@_auth(group='publish', viewfunc='views.publish_req')
@_auth(group='admin')
def publish(request):
    '''
    项目发布执行页
    '''
    project_list=Project.objects.all()
    action_list=Action.objects.all()
    #requester_list=Requester.objects.all()
    return render_to_response(
        'publish.html',
        locals()
    )

@_auth(group='publish')
def publish_req(request):
    '''
    项目发布申请页
    '''
    #多对多反查，已知用户查项目
    project_list=User.objects.get(
        username=request.user.username
    ).project_set.all()

    return render_to_response(
        'publish_req.html',
        locals()
    )

#@login_required(login_url='/')
@_auth()
def getaction(request):
    try:
        format = 'json'
        mimetype = 'application/json'

        # 多对多正查
        action=Project.objects.get(
            aliasname=request.POST['project']
        ).action.all()

        data = serializers.serialize(format, action)

        #return JsonResponse(data)
        return HttpResponse(data, mimetype)

    except Exception,e:
        #print(e)
        logger.error(e)


#@login_required(login_url='/')
@_auth()
def saltcall(request):
    try:
        project=request.POST.get('project','')
        action=request.POST.get('action','')
        sponsor=request.POST.get('sponsor','')
        Operator=request.POST.get('Operator','')
        detail=request.POST.get('detail','')
        P=Project.objects.filter(project_name=project)
        for a in P:
            project_id=a.id
        A=Action.objects.filter(action_name=action)
        for b in A:
            action_id=b.id
        S=Requester.objects.filter(requester_name=sponsor)
        for c in S:
            sponsor_id=c.id
        U=User.objects.filter(username=Operator)
        for d in U:
            username_id=d.id
        #万能的脚本呀
        cmd = "python script/run.py -o %s -x %s" % (project, action)
        status, msg = commands.getstatusoutput(cmd)
        status = 0 if status != 0 else 1
        wdb =  PAudit(
            project_id=project_id,
            action_id=action_id ,
            requester_id = sponsor_id,
            username_id = username_id,
            detail = detail,
            result = msg,
            status = status
        )
        wdb.save()
        return JsonResponse(
            {
                'status':status,
                'msg': msg
            }
        )
    except Exception,e:
        #print(e)
        logger.error(e)

# restful api
from rest_framework import viewsets
#import serializers
from serializers import UserSerializer
class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer

#=========
import aliyun
import aliyun.api

KEYID='KQVMzZVHTiSlj7f4'
KEYSECRET='lhIT0ADM7nXj3U05D2DoZCcFJ0pjvm'
#aliyuncli ecs DescribeRegions --output json 获取regionids
REGIONIDS=[
    'ap-southeast-1',
    'cn-shenzhen',
    'cn-qingdao',
    'cn-beijing',
    'cn-shanghai',
    'cn-hongkong',
    'cn-hangzhou',
    'us-west-1']
aliyun.setDefaultAppInfo(KEYID,KEYSECRET)

def EcsGet():
    a=aliyun.api.ecs.EcsDescribeInstancesRequest()
    for REGIONID in REGIONIDS:
        a.RegionId=REGIONID
        a.PageSize=50
        countpage=a.getResponse()['TotalCount']/a.PageSize\
                +1 if a.getResponse()['TotalCount']%a.PageSize\
                >0 else a.getResponse()['TotalCount']/a.PageSize
        for i in range(countpage, 0, -1):
            a.PageNumber=i
            ecsdata=a.getResponse()
            for Instance in ecsdata['Instances']['Instance']:
                PrivateIpAddress=''
                PublicIpAddress=''
                if Instance['InstanceNetworkType'] == 'classic':
                    for ip in Instance['PublicIpAddress']['IpAddress']:
                        PublicIpAddress=ip
                    for ip in Instance['InnerIpAddress']['IpAddress']:
                        PrivateIpAddress=ip
                else:
                    PublicIpAddress=Instance['EipAddress']['IpAddress']
                    for ip in Instance['VpcAttributes']['PrivateIpAddress']['IpAddress']:
                        PrivateIpAddress=ip
                try:
                    I=Idc.objects.filter(idc_name=Instance['RegionId'])
                    for i in I:
                        if PublicIpAddress:
                            wdb = Host(
                                public_address=PublicIpAddress,
                                private_address=PrivateIpAddress,
                                idc_id=i.id
                            )
                        else:
                            wdb = Host(
                                private_address=PrivateIpAddress,
                                idc_id=i.id
                            )
                        wdb.save()
                except Exception,e:
                    #logger.error(e)
                    print(e)
