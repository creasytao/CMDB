#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# © 2009-2016 ZHAN.com All Rights Reserved.
# @file        : Api/serializer.py
# @author      : Li90.COM
# @revision    : 2016-08-1 18:44:51
# @brief       :
from django.contrib.auth.models import *
from rest_framework import serializers
from Api.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
#from django.forms import widgets

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True,view_name='snippet-detail',read_only=True)
    class Meta:
        model = User
        fields = ('url','username', 'snippets')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

#class SnippetSerializer(serializers.Serializer):
#    pk = serializers.IntegerField(read_only=True)
#    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#    code = serializers.CharField(style={'base_template': 'textarea.html'})
#    linenos = serializers.BooleanField(required=False)
#    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#    def create(self, validated_data):
#        """
#        如果数据合法就创建并返回一个snippet实例
#        """
#        return Snippet.objects.create(**validated_data)
#
#    def update(self, instance, validated_data):
#        """
#        如果数据合法就更新并返回一个存在的snippet实例
#        """
#        instance.title = validated_data.get('title', instance.title)
#        instance.code = validated_data.get('code', instance.code)
#        instance.linenos = validated_data.get('linenos', instance.linenos)
#        instance.language = validated_data.get('language', instance.language)
#        instance.style = validated_data.get('style', instance.style)
#        instance.save()
#        return instance
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight',format='html')

    class Meta:
        model = Snippet
        fields = ('url','highlight','owner',
                  'title', 'code', 'linenos', 'language', 'style')
