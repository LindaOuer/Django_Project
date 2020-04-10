from django import forms

from .models import Student, User


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


class UserForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user']
