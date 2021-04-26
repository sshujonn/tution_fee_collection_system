from django.db import models
from django.contrib.auth.models import Group

from parent_menu.models import ParentMenu

# Create your models here.

class Menu(models.Model):
    menu_name = models.CharField(max_length=50)
    group = models.ManyToManyField(Group)
    related_url = models.CharField(max_length=50)
    parent_menu = models.ForeignKey(ParentMenu, on_delete=models.CASCADE)


