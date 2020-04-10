from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


# To get a better display of the group name
class PropertyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    STATUS = Group.objects.all()
    # print(STATUS)
    status = PropertyModelChoiceField(queryset=STATUS)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'status']
