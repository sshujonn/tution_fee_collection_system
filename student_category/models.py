from django.db import models


# Create your models here.
class StudentCategory(models.Model):
    student_category_name = models.CharField(max_length=50)
