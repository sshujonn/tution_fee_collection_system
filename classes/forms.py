from django.forms import ModelForm
from classes.models import StudentClass


class classForm(ModelForm):
    class Meta:
        model = StudentClass
        fields = ['class_name']
