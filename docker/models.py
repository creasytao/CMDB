#coding:utf-8
from django.db import models

# Create your models here.

class Instance(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True)
    net = models.CharField(
        max_length=20)
    private_ip = models.GenericIPAddressField(
        verbose_name='私有ip')
    inside_ip = models.GenericIPAddressField(
        unique=True,
        verbose_name='内部ip')
    float_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        unique=True,
        verbose_name='浮动ip')
    status = models.BooleanField(default=0)