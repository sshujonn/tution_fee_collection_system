from django.db import models


# Create your models here.

class StudentClass(models.Model):
    class_name = models.CharField(max_length=50)
    created_by = models.IntegerField(blank=False)
