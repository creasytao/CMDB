#coding:utf-8

from django.contrib import admin
#from django.contrib.admin.widgets import FilteredSelectMultiple
#from django.contrib.auth.models import User as djangouser, Group as djangogroup
from cmdb.models import *

class IdcAdmin(admin.ModelAdmin):
    list_display = (
        'idc_name',
        'sprovider',
        'region')
    search_fields = (
        'idc_name',
        'sprovider',
        'region')
    list_filter = (
        'idc_name',
        'sprovider',
        'region')

class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'service_name',
        'listen_port',
        'listen_socket',
        'script')
    search_fields = (
        'service_name',
        'listen_port',
        'listen_socket',
        'script')
    list_filter = (
        'service_name',
        'listen_port',
        'listen_socket',
        'script')

class HostAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = (
        'hostname',
        'public_address',
        'private_address',
        'idc',
        'ssh_port',
        'os')
    search_fields = (
        #'hostname',
        #'pubic_address',
        'private_address',
        #'ssh_port',
        'os',)
    list_filter = (
        #'hostname',
        #'public_address',
        #'private_address',
        'idc',
        'ssh_port',
        'os')
    #多对多字段复选框 水平排列
    filter_horizontal = ('hostgroup','service',)
    #外键字段 文本框展示
    raw_id_fields = ('idc',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'project_name',
        'aliasname')
    search_fields = (
        'project_name',
        'aliasname')
    list_filter = (
        'project_name',
        'aliasname')
    #多对多字段复选框 水平排列
    filter_horizontal = ('service','action',)

class ReadOnlyModelAdmin(admin.ModelAdmin):
    actions = None
    #save_on_top = False
    #save_as = True

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super(ReadOnlyModelAdmin, self).has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


class PAuditAdmin(ReadOnlyModelAdmin):
    list_per_page = 30
    list_display = (
        'StartTime',
        'project',
        'action',
        'requester',
        'username',
        'version',
        'detail',
        'result',
        'status')
    #外键search
    search_fields = [
        #'project__aliasname',
        #'action__aliasname',
        #'requester__requester_name',
        'version',
        'detail',
        'result']
    list_filter = (
        'StartTime',
        'project',
        'username',
        'requester',
        'action',
        'status')
    #日期过滤
    date_hierarchy = 'StartTime'
    ordering = ('-StartTime',)

#class RequestAdmin(admin.ModelAdmin):
#    list_per_page = 30
#    list_display = ('requester_name',)
#    search_fields = ('requester_name',)
#    list_filter = (
#        'requester_name',
#        'project')
    #多对多字段复选框 垂直排列
#    filter_vertical = ('project',)

class ActionAdmin(admin.ModelAdmin):
    list_per_page = 30
    #列表页显示的字段
    list_display = (
        'action_name',
        'aliasname')
    search_fields = (
        'action_name',
        'aliasname')
    list_filter = (
        'action_name',
        'aliasname')
    #详情单里字段显示及显示顺序
    fields = (
        'aliasname',
        'action_name')

admin.site.register(Idc,IdcAdmin)
admin.site.register(HostGroup)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Action,ActionAdmin)
#admin.site.register(Requester,RequestAdmin)
admin.site.register(PAudit,PAuditAdmin)

#管理django_admin_log
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.models import User

action_names = {
    ADDITION: '增加',
    CHANGE:   '修改',
    DELETION: '删除',
}

class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
            return queryset.filter(**dictionary)

class ActionFilter(FilterBase):
    title = '操作类型'
    parameter_name = 'action_flag'
    def lookups(self, request, model_admin):
        return action_names.items()

class UserFilter(FilterBase):
    title = '用户'
    parameter_name = 'user_id'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username)
            for u in User.objects.filter(pk__in =
                LogEntry.objects.values_list('user_id').distinct())
        )

class AdminFilter(UserFilter):
    title = '超级用户'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_superuser=True))

class StaffFilter(UserFilter):
    title = '组用户'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_staff=True))


class LogEntryAdmin(ReadOnlyModelAdmin):
    list_per_page = 30
    list_display = (
        'action_time',
        'user',
        'content_type',
        #'object_repr',
        'action_description',
        'change_message',
        'object_link',)
    search_fields = [
        'object_repr',
        'change_message']
    list_filter = [
        ActionFilter,
        'content_type',
        UserFilter,
        AdminFilter,
        StaffFilter,]
    date_hierarchy = 'action_time'
    ordering = ('-action_time',)

    def object_link(self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id])
            link = u'<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return link if obj.action_flag != DELETION else repr_
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'


admin.site.register(LogEntry, LogEntryAdmin)
