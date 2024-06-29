from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Form for Registration below
class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Please enter a valid email address')

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2')
