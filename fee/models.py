from django.db import models


# Create your models here.
class Fee(models.Model):
    fee_name = models.CharField(max_length=50)
    fee_amount = models.CharField(max_length=10)
