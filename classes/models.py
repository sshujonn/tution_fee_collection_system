from django.db import models
from branches.models import Branch

# Create your models here.

class StudentClass(models.Model):
    class_name = models.CharField(max_length=50)
    created_by = models.IntegerField(blank=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name
