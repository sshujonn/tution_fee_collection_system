from django.forms import ModelForm, TextInput
from classes.models import StudentClass


class classForm(ModelForm):
    class Meta:
        model = StudentClass
        fields = ['class_name']
