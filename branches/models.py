from django.db import models


# Create your models here.

class Branch(models.Model):
    branch_name = models.CharField(max_length=50)
    branch_email = models.CharField(max_length=60)
    branch_phone_number = models.CharField(max_length=20)
    branch_address = models.CharField(max_length=100)
    branch_status = models.CharField(max_length=100)
