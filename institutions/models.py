from django.db import models

# Create your models here.


class Institution(models.Model):
    institution_name = models.CharField(max_length=150)
    institution_address = models.CharField(max_length=200)
    institution_phone_number = models.CharField(max_length=30)

