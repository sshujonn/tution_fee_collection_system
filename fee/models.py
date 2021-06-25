from django.db import models
from classes.models import StudentClass

# Create your models here.
class Fee(models.Model):
    fee_name = models.CharField(max_length=50)
    fee_amount = models.CharField(max_length=10)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
