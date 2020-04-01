import datetime as dt
from django import forms
from .models import Preferred_Times
from .times import TIMES_CHOICES

class CreateUpdatePreferredTimesForm(forms.ModelForm):
    class Meta:
        model = Preferred_Times
        exclude = ('allowed_route_id','id')
        widgets = {'mon_a_to_b': forms.Select(choices=TIMES_CHOICES),
            'tues_a_to_b': forms.Select(choices=TIMES_CHOICES),
            'wed_a_to_b': forms.Select(choices=TIMES_CHOICES),
            'thurs_a_to_b': forms.Select(choices=TIMES_CHOICES),
            'fri_a_to_b': forms.Select(choices=TIMES_CHOICES),
            'sat_a_to_b': forms.Select(choices=TIMES_CHOICES),
            'sun_a_to_b': forms.Select(choices=TIMES_CHOICES),
            'mon_b_to_a': forms.Select(choices=TIMES_CHOICES),
            'tues_b_to_a': forms.Select(choices=TIMES_CHOICES),
            'wed_b_to_a': forms.Select(choices=TIMES_CHOICES),
            'thurs_b_to_a': forms.Select(choices=TIMES_CHOICES),
            'fri_b_to_a': forms.Select(choices=TIMES_CHOICES),
            'sat_b_to_a': forms.Select(choices=TIMES_CHOICES),
            'sun_b_to_a': forms.Select(choices=TIMES_CHOICES),
        }