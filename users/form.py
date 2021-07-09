from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from users.models import Profile


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='First Name. Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Last Name. Optional.')
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    first_name = forms.CharField(max_length=100,
                                widget=forms.TextInput
                                (attrs={'class': 'form-control',
                                        'id': 'user-name', 'placeholder': 'Username'}))
    last_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput
                                 (attrs={'class': 'form-control',
                                         'id': 'last-name'}))
    email = forms.CharField(max_length=100,
                                 widget=forms.EmailInput
                                 (attrs={'class': 'form-control',
                                         'id': 'email'}))

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
