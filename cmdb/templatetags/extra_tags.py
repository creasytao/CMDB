#coding:utf-8
from django import template
register = template.Library()

import datetime
@register.filter
def chinese_date_format(value,format):
    # dateArray = datetime.datetime.utcfromtimestamp(value)
    dateArray = datetime.datetime.fromtimestamp(value)
    otherStyleTime = dateArray.strftime(format)
    return otherStyleTime
