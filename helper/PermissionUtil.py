from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import exceptions


def check_permission(request, action, module):
    try:
        name = module[1]
        groups = User.objects.get(pk=request.user.id).groups.all()
        # import pdb;pdb.set_trace()
        if action == ("detail" or "view") or module[0] == "view":
            codename = "view_{name}".format(name=name)
        elif action == "update" or action == "change":
            codename = "change_{name}".format(name=name)
        elif action == "delete" or  action == "remove":
            codename = "delete_{name}".format(name=name)
        elif module[0] == "create" or module[0] == "add":
            codename = "add_{name}".format(name=name)
        else:
            return False
        permission = False
        # import pdb;
        # pdb.set_trace()
        for group in groups:
            permission = permission or group.permissions.filter(codename=codename).exists()
        # import pdb;pdb.set_trace()
        return permission
    except Exception as ex:

        return False


class DBCRUDPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # import pdb;
        # pdb.set_trace()
        action = request.resolver_match.kwargs.get('action')
        module = request.resolver_match.url_name.split("_")


        return check_permission(request, action, module)
