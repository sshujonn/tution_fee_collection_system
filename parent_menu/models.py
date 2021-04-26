from django.db import models

# Create your models here.
class ParentMenu(models.Model):
    p_menu_name = models.CharField(max_length=50)