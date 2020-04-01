from django import forms
from django.utils.translation import gettext_lazy

class SubmitCommuterID(forms.Form):
    commuter_number = forms.IntegerField()

class SubmitRouteID(forms.Form):
    route_number = forms.IntegerField()