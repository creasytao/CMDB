#coding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
#from cmdb.views import views as cmdb_views
from views import views as cmdb_views
from django.contrib.auth import views as auth_views

admin.autodiscover()


from rest_framework import routers

router = routers.DefaultRouter()
#router.register(r'users', cmdb_views.views.UserViewSet)
#router.register(r'users', cmdb_views.UserViewSet)


import settings
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.site_url = settings.ADMIN_SITE_URL

urlpatterns = patterns('',
    #重置密码
    url(r'^admin/password_reset/$',
        auth_views.password_reset,
        name='admin_password_reset'),
    url(r'^admin/password_reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
       name='password_reset_complete'),
    url(r'^accounts/login/$', cmdb_views.login),
    #账号管理
    url(r'^login/$', cmdb_views.login),
    url(r'^logout/$', cmdb_views.logout),
    url(r'^changepwd/$', cmdb_views.changepwd),
    #业务
    url(r'^dashboard/$', cmdb_views.dashboard),
    url(r'^assets/$', cmdb_views.assets),
    url(r'^assets/hostlist/$', cmdb_views.assets_hostlist),
    url(r'^assets/topology/$', cmdb_views.assets_topology),
    url(r'^configure/$', cmdb_views.configure),
    url(r'^publish/$', cmdb_views.publish),
    url(r'^audit/$', cmdb_views.audit),

    url(r'^saltcall/$', cmdb_views.saltcall),
    url(r'^getaction/$', cmdb_views.getaction),
    url(r'^requester/$', cmdb_views.Requester),

    url(r'^k8shelm/$',cmdb_views.helm_list),

    #RESTfull API 相关
    url(r'^api/', include(router.urls)),
    #主页及后台
    url(r'^$', cmdb_views.index),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
