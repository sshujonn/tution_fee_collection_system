from django.db import models


# Create your models here.
class student_category(models.Model):
    student_category_name = models.CharField(max_length=50)
