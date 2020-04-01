from django import forms
from django.contrib.auth.models import User
from .models import Cities
from employees.models import Employees

class CreateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ('first_name', 'middle_name', 'last_name', 'department', 'job_title')

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),
        help_text='* employees can change their password later on')
    class Meta():
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None,
        }

class UpdateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Cities
        fields = ('major_announcement', 'minor_announcement', 'major_is_active', 'minor_is_active')
        