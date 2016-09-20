#coding:utf-8
"""
Django settings for djangoproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ConfigParser
config = ConfigParser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
config.read(os.path.join(BASE_DIR, 'config'))

ADMIN_SITE_HEADER = config.get('admin', 'header')
ADMIN_SITE_TITLE = config.get('admin','title')
ADMIN_SITE_URL = config.get('admin','site_url')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = config.getboolean('mail','email_use_tls')
EMAIL_HOST = config.get('mail','email_host')
EMAIL_PORT = config.getint('mail','email_port')
EMAIL_HOST_USER = config.get('mail','email_host_user')
EMAIL_HOST_PASSWORD = config.get('mail','email_host_password')
DEFAULT_FROM_EMAIL = config.get('mail','default_from_email')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = config.get('base','secret_key')
SECRET_KEY = 'lfl145r(_0aaow+%(#ju6=c*95t8ckaim=%76!0k#7o0*cqg!l))'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('base','debug')

TEMPLATE_DEBUG = config.getboolean('base','template_debug')

ALLOWED_HOSTS = config.get('base','allowed_hosts')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'bootstrap_toolkit',
    'cmdb',
#    'users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', #本地语言
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'djangoproject.urls'

WSGI_APPLICATION = 'djangoproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	'ENGINE': 'django.db.backends.mysql',
	'NAME': config.get('db','database'),
	'USER': config.get('db','username'),
	'PASSWORD': config.get('db','password'),
	'HOST': config.get('db','host'),
    },
#    'slave': {
#	'ENGINE': 'django.db.backends.mysql',
#	'NAME': 'django',
#	'USER': 'django',
#	'PASSWORD': '123456',
#	'HOST': '192.168.88.92',
#    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh_CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
#影响date_hierarchy
USE_TZ = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = config.getboolean('session','session_expire_at_browser_close')
#SESSION_COOKIE_AGE = config.get('session','session_cookie_age')
#SESSION_COOKIE_AGE = 30 * 60

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'



TEMPLATE_DIRS = (
	os.path.join(BASE_DIR,'templates'),
)
STATICFILES_DIRS = (
	os.path.join(BASE_DIR,'static'),
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser'
    ],
    'PAGE_SIZE': 10
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

