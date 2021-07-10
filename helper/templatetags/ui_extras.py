import datetime

import pytz
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter, register
from django.urls import reverse

from helper.constant import CURRENT_SITE_URL


@register.filter
@stringfilter
def int_to_string(value):
    return value


@register.filter()
def to_int(value):
    return int(value)



@register.filter
def static_address_generate_from_name(value): #this one is from str
    return value.replace("static/", "")

@register.filter
def local_time(user):
    format = '%Y-%m-%d %I:%M:%S %p'
    utc = pytz.utc
    utc_date = user.updated_at.replace(tzinfo=utc)  # tz aware
    local_time =  utc_date.astimezone(pytz.timezone(user.time_zone)).replace(microsecond=0).replace(tzinfo=None)
    my_time = datetime.datetime.strftime(local_time, format)
    return str(my_time)

@register.filter
def change_lan_code(lan_url):
    if '/en' in lan_url:
        return lan_url.replace('/en','')
    elif '/ja' in lan_url:
        return lan_url.replace('/ja', '')
    return lan_url

@register.filter
def change_seconds_to_hour_min_sec(seconds):
    intervals = (
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:4])


@register.filter
def get_create_permission_or_false(module,request):
    user = User.objects.get(pk = request.user.id)
    groups = user.groups.all()
    for group in groups:
        if group.permissions.filter(codename="add_" + module).exists():
            return True
    return False

@register.filter
def get_edit_permission_or_false(module,request): #returns false if permission available
    user = User.objects.get(pk = request.user.id)
    groups = user.groups.all()
    for group in groups:
        if group.permissions.filter(codename="change_" + module).exists():
            return True
    return False

@register.filter
def get_delete_permission_or_false(module,request): #returns false if permission available
    user = User.objects.get(pk = request.user.id)
    groups = user.groups.all()
    for group in groups:
        if group.permissions.filter(codename="delete_" + module).exists():
            return True
    return False

@register.filter
def get_user_group_exists_or_not(value,request):
    # import pdb;pdb.set_trace()
    if value:
        if request.user.groups.filter(name__iregex=value).exists():
            return True
    return False