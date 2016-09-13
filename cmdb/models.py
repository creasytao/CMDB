#coding:utf-8

from __future__ import unicode_literals, absolute_import
import cPickle as pickle

from django.db import models
from django.contrib.auth.models import User

class Idc(models.Model):
    '''
    idc表
        idc_name:全局唯一，程序识别
        sprovider:提供商
        region:地域
    隐藏id字段为host表外键
    '''
    idc_name = models.CharField(
        max_length=50,
        unique=True)
    sprovider = models.CharField(max_length=50,
                                 verbose_name='服务提供商')
    region = models.CharField(max_length=100,
                              verbose_name='地域')

    def __unicode__(self):
        return self.idc_name

class Group(models.Model):
    group_name = models.CharField(
        max_length=50,
        unique=True)

    def __unicode__(self):
        return self.group_name

class Service(models.Model):
    service_name = models.CharField(
        max_length=50,
        unique=True)
    toplevel = models.CharField(max_length=50,
                                verbose_name='工作层级')
    listen_port = models.IntegerField(
        null=True,
        blank=True)
    listen_socket = models.CharField(
        max_length=200,
        null=True,
        blank=True)
    script = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='管理脚本')

    def __unicode__(self):
        return self.service_name

    def save(self, *args, **kwargs):
        if not self.listen_port:self.listen_port = None
        if not self.listen_socket:self.listen_socket = None
        if not self.script:self.script = None
        super(Service, self).save(*args, **kwargs)

class Host(models.Model):
    hostname = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        unique=True)
    private_address = models.GenericIPAddressField(
        unique=True,
        verbose_name='私有ip地址')
    public_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        unique=True,
        verbose_name='公有ip地址')
    idc = models.ForeignKey(Idc)
    group = models.ManyToManyField(
        Group,
        blank=True)
    service = models.ManyToManyField(
        Service,
        blank=True)
    ssh_port=models.IntegerField(
        default=22,
        verbose_name='ssh登陆端口')
    os=models.CharField(
        max_length=20,
        default='linux',
        verbose_name='操作系统版本')

    def __unicode__(self):
        return self.private_address

    def save(self, *args, **kwargs):
        if not self.hostname:self.hostname = None
        if not self.public_address:self.public_address = None
        super(Host, self).save(*args, **kwargs)

class Action(models.Model):
    action_name = models.CharField(
        max_length=30,
        unique=True)
    aliasname = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='操作别名')

    def __unicode__(self):
        return self.aliasname

    def save(self, *args, **kwargs):
        if not self.aliasname:self.aliasname = None
        super(Action, self).save(*args, **kwargs)

class Project(models.Model):
    project_name = models.CharField(
        max_length=100,
        unique=True)
    aliasname = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='项目别名')
    service = models.ManyToManyField(
        Service,
        blank=True)
    action = models.ManyToManyField(
        Action,
        blank=True)

    def __unicode__(self):
        return self.aliasname

    def save(self, *args, **kwargs):
        if not self.project_name:self.project_name = None
        if not self.aliasname:self.aliasname = None
        super(Project, self).save(*args, **kwargs)

class Requester(models.Model):
    '''
    项目发布申请人
    '''
    requester_name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='申请人')
    project = models.ManyToManyField(
        Project,
        blank=True,
        verbose_name='申请项目')
    def __unicode__(self):
        return self.requester_name

class PAudit(models.Model):
    '''
    项目审计
    '''
    time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        Project,
        related_name='pa_p',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    action = models.ForeignKey(
        Action,
        related_name='pa_c',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    requester = models.ForeignKey(
        Requester,
        related_name='pa_s',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='申请人'
    )
    username = models.ForeignKey(
        User,
        related_name='pa_u',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='操作人'
    )
    version = models.CharField(max_length=25,
                               verbose_name='版本号')
    detail = models.TextField(max_length=1000,
                             verbose_name='上线说明')
    result = models.TextField(max_length=1000,
                             verbose_name='操作结果')
    status = models.BooleanField(default=0)
