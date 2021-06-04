from coreapi import Object
from django.contrib.auth.models import Group

from rest_framework.permissions import BasePermission

from menu.models import Menu



class GroupBasePermission(BasePermission):
    def check_permission(self, user):
        pass

class GlobalService(Object):
    def update_immutable_obj(self, obj, kwargs):
        mutability_state = obj._mutable
        obj._mutable = True
        for k, v in kwargs.items():
            obj.update({k:v})
        obj._mutable = mutability_state
        return obj

    def get_menu(self, user):
        groups = user.groups.all()
        menus = Menu.objects.filter(group__in=groups)
        result = {}
        for menu in menus:
            p_menu_name = menu.parent_menu.p_menu_name
            if not result.get(p_menu_name):
                result[p_menu_name] = []
                if {'menu_name':menu.menu_name, 'url': menu.related_url} not in result.get(p_menu_name):
                    result[p_menu_name].append({'menu_name':menu.menu_name, 'url': menu.related_url})
            else:
                if {'menu_name':menu.menu_name, 'url': menu.related_url} not in result.get(p_menu_name):
                    result[p_menu_name].append({'menu_name':menu.menu_name, 'url': menu.related_url})
        return result