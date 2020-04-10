from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Student


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        # exclude = ['email']
        help_texts = {
            'lastName': 'Your name here!',
        }
        error_messages = {
            'lastName': {
                'max_length': "This student's name is too long.",
            },

        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
