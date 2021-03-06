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
from django.core.mail import send_mail


#from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.decorators import login_required
from mywrapper import _auth

from forms import *
from ..settings import *
import yaml
from cmdb.models import *
import os, sys, commands, json
from pyhelm.tiller import Tiller
from pyhelm.repo import RepoUtils
from pyhelm.chartbuilder import ChartBuilder

import re
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
    #else
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(
            username=username,
            password=password
        )
        if user is not None and user.is_active:
            auth.login(request, user)
            if re.match( r'^/login(/)?$', request.path):
                return HttpResponseRedirect('/')
            #else
    	    return HttpResponseRedirect(request.path)
        #else
        password_is_wrong = True
        return render_to_response(
            'login.html',
            locals()
        )
    #else
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
            oldpassword = form.cleaned_data['oldpassword']
            user = auth.authenticate(
                username=username,
                password=oldpassword
            )
            if user is not None and user.is_active:
                newpassword = form.cleaned_data['newpassword1']
                user.set_password(newpassword)
                user.save()
		return HttpResponseRedirect(redirect_to)
            else:
                oldpassword_is_wrong = True
                return render_to_response(
                    'changepwd.html',
                    locals()
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

def Paging(lines, size, page):
    '''
    分页函数
    '''
    paginator = Paginator(lines, size)
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = Paginator.page(paginator.num_pages)
    return show_lines

#@login_required(login_url='/')
@_auth(group="admin",viewfunc='views.assets_hostlist_admin')
def assets_hostlist(request):
    lines=Host.objects.all().order_by("id")
    page = request.GET.get('page')

    return render_to_response(
        'hostlist.html',
        {'show_lines':Paging(lines, 15, page),
         'request':request}
    )

@_auth(group="admin")
def assets_hostlist_admin(request):
    update = request.GET.get('update', False)
    if update:
        EcsGet()
    lines=Host.objects.all().order_by("id")
    page = request.GET.get('page')

    return render_to_response(
        'hostlist.html',
        {'show_lines':Paging(lines, 15, page),
         'request':request,
         'update':True}
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
@_auth(group='publish', viewfunc='views.audit_req')
@_auth(group='admin')
def audit(request):
    paudit_id = request.GET.get('paudit_id')

    result_id =  request.GET.get('result')
    if result_id:
        paudit = PAudit.objects.filter(id=result_id)
        for i in paudit:
            paudit_result=i.result
            return render_to_response('format_retrun.html',{'data':paudit_result,'request':request})

    if paudit_id:
        paudit = PAudit.objects.filter(id=paudit_id)
        data = []
        for i in paudit:
            data.append({'id':paudit_id,
                        'project':i.project.aliasname,
                         'action':i.action.aliasname,
                         'version':i.version,
                         'requester':i.requester.username,
                         'detail':i.detail
                        })
        return publish(request,data=data)
        #return publish(request)

    lines = PAudit.objects.all().order_by("-StartTime")
    page = request.GET.get('page')
    link = True
    return render_to_response(
        'audit.html',
        {
            'show_lines': Paging(lines, 10, page),
            'request': request,
            'link':link
        }
    )

#@login_required(login_url='/')
@_auth(group='publish')
def audit_req(request):
    result_id =  request.GET.get('result')
    if result_id:
        paudit = PAudit.objects.filter(id=result_id)
        for i in paudit:
            paudit_result=i.result
            return render_to_response('format_retrun.html',{'data':paudit_result,'request':request})
    #多对多反查，已知用户查项目
    project = User.objects.get(
        username=request.user.username
    ).project_set.all()
    data = []
    for i in project:
        p=PAudit.objects.filter(project__id=i.id)
        for j in p:
            data.append({'id':j.id,
                        'StartTime':j.StartTime,
                         'EndTime':j.EndTime,
                         'project':j.project,
                         'action':j.action,
                         'requester':j.requester,
                         'username':j.username,
                         'version':j.version,
                         'detail':j.detail,
                         'result':j.result,
                         'status':j.status
                        })

    lines = sorted(data, key= lambda x:x['StartTime'], reverse = True)
    page = request.GET.get('page')
    return render_to_response(
        'audit.html',
        {
            'show_lines': Paging(lines, 10, page),
            'request': request
        }
    )


#@login_required(login_url='/')
@_auth(group='publish', viewfunc='views.publish_req')
@_auth(group='admin')
def publish(request, *agrgs, **kwargs):
    '''
    项目发布执行页
    '''
    if kwargs:
        if kwargs['data']:
            for i in kwargs['data']:
                paudit_id=i['id']
                project=i['project']
                action=i['action']
                version=i['version']
                detail=i['detail']
                requester=i['requester']
            return render_to_response(
                'publish_call.html',
                locals()
            )

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
# @_auth(group='publish')
# @_auth(group='admin')
def helm_list(request):
    ins = Tiller(K8S_HOST, K8S_PORT)
    if request.method == 'GET':
        # print 'GET'
        # chart_path = RepoUtils.from_repo(CHART_REPO,'jenkins')
        # print chart_path


        action = request.GET.get('action', False)
        name = request.GET.get('name', None)
        if action == 'detail':
            release_status = ins.get_release_status(name)
            release_content = ins.get_release_content(name)
            release_history = ins.get_history(name)
            # print release_history.releases[0]
            resource = [
                {
                    "type": yaml.load(x)['kind'],
                    "content": x
                }
                for x in release_content.release.manifest.split('---') if yaml.load(x)
            ]
            # print resource
            # resource = [ x for x in release_content.release.manifest.split('---')]
            # release_history.releases[0]
            return render(
                request,'helm_detail.html',
                {
                    "status": release_status,
                    "content": release_content,
                    "history": release_history.releases,
                    "resource": resource,
                    "request": request
                }

            )
        list = ins.list_releases()
        return render(
            request,'helm_publish.html',
            {
                "list_name": list,
                "request": request
            })
    action = request.POST.get('action', None)
    name = request.POST.get('name',None)
    if action == 'rollback':
        version = request.POST.get('version',None)
        # print type(version)
        try:
            rollback_result = ins.rollback_release(name=name,version=int(version))
        except Exception,e:
            print e
        print rollback_result
        return JsonResponse({'result': rollback_result})
    if action == 'install':
        # pass
        namespace = request.POST.get('namespace', None)
        chartname = request.POST.get('chartname', None)
        deployname = request.POST.get('deployname', None)
        values = request.POST.get('values', None)
        chart_path = RepoUtils.from_repo(CHART_REPO, chartname)
        chart = ChartBuilder({'name': chartname, 'source': {'type': 'directory', 'location': chart_path}})
        try:
            result = ins.install_release(chart.get_helm_chart(),namespace,name=deployname,values=values)
        except Exception,e:
            result = e
        return JsonResponse({'result': result})
    if action == 'update':
        chartname = request.POST.get('chartname', None)
        deployname = request.POST.get('deployname', None)
        values = request.POST.get('values', None)
        chart_path = RepoUtils.from_repo(CHART_REPO, chartname)
        chart = ChartBuilder({'name': chartname, 'source': {'type': 'directory', 'location': chart_path}})
        try:
            result = ins.update_release(chart.get_helm_chart(), deployname, values=values)
        except Exception,e:
            result = e
        return JsonResponse({'result': result})




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

@_auth()
def Requester(request):
    '''
    提交发布申请
    '''
    try:
        project = request.POST.get('project', None)
        action = request.POST.get('action', None)
        version = request.POST.get('version', None)
        requester = request.POST.get('requester', None)
        detail = request.POST.get('detail', None)
        Project.objects.get(aliasname=project)
        pa = PAudit(
            project = Project.objects.get(aliasname=project),
            action = Action.objects.get(aliasname=action),
            version = version,
            requester = User.objects.get(username=requester),
            detail = detail
        )
        pa.save()
        group = Group.objects.get(name='admin')
        users = group.user_set.all()
        dstemail = []
        for user in users:
            dstemail.append(user.email)
        send_mail('发布申请',"项目："+project+"\n动作："+action+
                  "\n详细描述："+detail+"\n\t\t\t申请人："+requester,
                  DEFAULT_FROM_EMAIL,dstemail)
        return JsonResponse({'your_msg':'提交成功'})
    except Exception, e:
        logger.error(e)
        return JsonResponse({'your_msg':'谁在搞飞机'})



#@login_required(login_url='/')
@_auth()
def saltcall(request):
    try:
        paudit_id=request.GET.get('paudit_id', None)
        project=request.POST.get('project','')
        action=request.POST.get('action','')
        requester=request.POST.get('requester','')
        Operator=request.POST.get('Operator','')
        #detail=request.POST.get('detail','')

        P=Project.objects.filter(aliasname=project)
        for a in P:
            project_name=a.project_name
        A=Action.objects.filter(aliasname=action)
        for b in A:
            action_name=b.action_name
        #万能的脚本呀
        #cmd = "python script/run.py -o %s -x %s" % (project_name, action_name)
        cmd = "hostname"
        status, msg = commands.getstatusoutput(cmd)
        status = 0 if status != 0 else 1

        obj = PAudit.objects.get(id=paudit_id)
        obj.username=User.objects.get(username=Operator)
        obj.result=msg
        obj.status=status
        obj.save()
        users = User.objects.filter(username=requester)
        dstemail=[]
        for user in users:
            dstemail.append(user.email)
        send_mail('发布完成',"项目："+project+"\n动作："+action+
                  "\n操作结果："+msg+"\n\t\t\t操作人："+Operator,
                  DEFAULT_FROM_EMAIL,dstemail)
        return JsonResponse(
            {
                'status':status,
                'msg': msg
            }
        )
    except Exception,e:
        logger.error(e)

# restful api
from rest_framework import viewsets
#import serializers
from serializers import UserSerializer
class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer

#===============================
# 阿里云资产
#================================
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
#=============================
# 青云资产
#============================

def MyPagination(total, size):
    countpage = total/size +1 if total%size >0 else total/size
    return countpage

class QingCloud:
    def __init__(self, zone, access_key_id, secret_access_key, pagesize=20):
        import qingcloud.iaas
        self.data = {}
        self.zone = zone
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.pagesize = pagesize
        self.conn = qingcloud.iaas.connect_to_zone(
            self.zone, self.access_key_id, self.secret_access_key, lowercase=True
        )

    def GetData(self, object):
        self.data[object] = []
        myfunc = getattr(self.conn, "describe_%ss" % object)
        for i in range(MyPagination(myfunc()['total_count'], self.pagesize)):
            self.data[object].extend(
                myfunc(offset=i*self.pagesize, limit=self.pagesize)["%s_set" % object]
            )

    def WriteToDb(self, ):
        pass

    def ViewsDb(self, ):
        pass

    def ClearMEM(self, object=''):
        if object:
            self.data[object] = []
            return
        self.data = {}

class WriteDB(QingCloud):
    def Instance(self, ):
        for i in self.data['instance']:
            private_ip, vcpus_current, memory_current, os_family, instance_id = '','','','',''
            instance_name = i['instance_name']
            instance_id = i['instance_id']
            vcpus_current = i['vcpus_current']
            memory_current = i['memory_current']
            os_family = i['image']['os_family']
            status = i['status']
            if i['vxnets']:
                vxnet_name, private_ip = i['vxnets'][0]['vxnet_name'], i['vxnets'][0]['private_ip']
            else:
                vxnet_name = private_ip = ''
            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (instance_id, vcpus_current, memory_current, os_family, status, private_ip, vxnet_name, instance_name)
            wdb = Host(

            )

'''

n=QingCloud('PEK3A','LORLHQIRZXQZRLLOJBIW','JsEIDxauDgDIq77OlmQ36U6LFUnXWOFE0vl6muLv')
instances=n.GetData('instance')



        volumes = conn.describe_volumes()
        status = volumes[u'volume_set'][0]['status']
        size = volumes[u'volume_set'][0]['size']
        instance_id = volumes[u'volume_set'][0]['instance']['instance_id']

    private_ip = instances['instance_set'][0]['vxnets'][0]['private_ip']
    vcpus_current = instances['instance_set'][0]['vcpus_current']
    memory_current = instances['instance_set'][0]['memory_current']
    os_family = instances['instance_set'][0]['image']['os_family']
    instance_id = instances['instance_set'][0]['instance_id']


        a=instances.
'''