from re import search

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')
        labels = {
            'confirm_password':"Confirm Password",
        }
        help_texts = {
            'username':None,
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username

        raise forms.ValidationError("This username has already been taken", 'username_duplicate')

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 6:
            raise forms.ValidationError('Your password must be at least 6 characters long and contain at least one number and one letter of any case', 'password_length')
        elif not search(r'^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$', password):
            raise forms.ValidationError('Your password must contain at least one letter of any case and one number', 'password_strength')

        return password

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "passwords do not match"
            )