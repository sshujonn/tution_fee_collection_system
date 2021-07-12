from django.db import models

# Create your models here.
from classes.models import StudentClass
from students.models import students


class Payment(models.Model):
    year = models.CharField(max_length=30)
    month = models.CharField(max_length=20)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    student = models.ForeignKey(students, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
