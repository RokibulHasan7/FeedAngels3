from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import CharField

from .models import CustomUser


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, help_text='Required. 100 charaters of fewer.', widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('full_name', 'mobileNum', 'email')

