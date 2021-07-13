from django.db import models
from classes.models import StudentClass


# Create your models here.
class sections(models.Model):
    section_name = models.CharField(max_length=30)
    section_shift = models.CharField(max_length=20)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.section_name