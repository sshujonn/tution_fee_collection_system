from django.db import models
from sections.models import sections
from student_category.models import StudentCategory
from classes.models import StudentClass

# Create your models here.
class bill_generation(models.Model):
    CLASS_ID = models.CharField(max_length=50)
    STUDENT_ID = models.CharField(max_length=20)
    FEE_ID = models.CharField(max_length=100)
    FEE_AMOUNT = models.CharField(max_length=10)
    SESSION_START_DATE = models.DateTimeField()
    SESSION_END_DATE = models.DateTimeField()
    BILLING_MONTH = models.DateTimeField()
    MAKER_TIME = models.DateTimeField()


    # section = models.ForeignKey(sections, on_delete=models.CASCADE)
    # # section = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    # category = models.ForeignKey(StudentCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_name