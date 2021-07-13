from django.db import models
from sections.models import sections
from student_category.models import StudentCategory
from classes.models import StudentClass

# Create your models here.
class students(models.Model):
    student_name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=20)
    student_email = models.CharField(max_length=100)
    student_gender = models.CharField(max_length=10)
    student_dob = models.DateTimeField()
    student_address = models.CharField(max_length=100)
    student_religion = models.CharField(max_length=20)
    student_father_name = models.CharField(max_length=50)
    student_mother_name = models.CharField(max_length=50)
    session_start_date = models.DateTimeField()
    session_end_date = models.DateTimeField()
    section = models.ForeignKey(sections, on_delete=models.CASCADE)
    # section = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    category = models.ForeignKey(StudentCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_name