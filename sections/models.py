from django.db import models


# Create your models here.
class sections(models.Model):
    section_name = models.CharField(max_length=30)
    section_shift = models.CharField(max_length=20)
