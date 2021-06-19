from django.db import models

from institutions.models import Institution

# Create your models here.

class Branch(models.Model):
    branch_name = models.CharField(max_length=50)
    branch_email = models.CharField(max_length=60)
    branch_phone_number = models.CharField(max_length=20)
    branch_address = models.CharField(max_length=100)
    branch_status = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch_name
