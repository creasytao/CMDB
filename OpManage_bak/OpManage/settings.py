#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# © 2009-2016 ZHAN.com All Rights Reserved.
# @file        : OpManage/settings.py
# @author      : Li90.COM
# @revision    : 2016-08-1 18:44:51
# @brief       :
"""
Django settings for OpManage project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sou!vgfduy)*s*ay#_ylj_xm*&i**nyc7w-5m6-($0t%73qt+^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OpManage.urls'

WSGI_APPLICATION = 'OpManage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
                'NAME': 'OpManage',
                'USER': 'root',
                'PASSWORD': '123456',
                'HOST': '192.168.88.92',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#自动加／
APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK={
    'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY':10,



}

import logging
import django.utils.log
import logging.handlers


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
       'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  #日志格式
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/all.log',               #日志输出文件
            'maxBytes': 1024*1024*5,                  #文件大小
            'backupCount': 5,                         #备份份数
            'formatter':'standard',                   #使用哪种formatters日志格式
        },
        'error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'maxBytes':1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/access.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'logs/script.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'sourceDns.webdns.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'sourceDns.webdns.util':{
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}
