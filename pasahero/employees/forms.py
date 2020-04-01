from django import forms
from django.forms import formset_factory

from .times import TIME_OPTIONS_FOR_EMPLOYEES
from transportations.models import Routes, Directions, Times

class CreateDirectionForm(forms.ModelForm):
    class Meta:
        model = Directions
        fields = ('start_location', 'end_location', 'vehicle', 'duration_minutes')

class CreateRouteForm(forms.ModelForm):
    class Meta:
        model = Routes
        fields = ('name', 'via', 'point_a', 'point_b')
        help_texts = {
            "name":"Ex: Quezon City Circle - Araneta Avenue",
            "via":"Ex: Quezon Avenue",
            "point_a":"Ex: Quezon City Circle",
            "point_b":"Ex: Araneta Avenue",
        }
        labels = {
            "name":"Displayed Route Name",
            "point_a":"Point A",
            "point_b":"Point B",
        }

class CreateDirectionForm(forms.ModelForm):
    class Meta:
        model = Directions
        fields = ('start_location', 'end_location', 'vehicle', 'duration_minutes')

class CreateTimesForm(forms.ModelForm):
    class Meta:
        model = Times
        fields = ('time', 'capacity')
        widgets = {'time': forms.DateInput(attrs={'class':'form-control', 'type':'time'}),
        }

CreateTimeFormSet = formset_factory(CreateTimesForm, extra=5, min_num=1)