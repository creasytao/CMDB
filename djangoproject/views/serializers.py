#coding:utf-8

from django.contrib.auth.models import User
from rest_framework import serializers



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'last_login',
            'is_superuser',
            'username',
            'email',
            'is_staff',
            'is_active',
            'date_joined')


