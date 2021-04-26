from rest_framework import serializers

from menu.models import Menu
from parent_menu.models import ParentMenu


class ParentMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentMenu
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    # parent_menu = ParentMenuSerializer(serializers.ModelSerializer)
    class Meta:
        model = Menu
        fields = (
            'id', 'menu_name', 'parent_menu'
        )
