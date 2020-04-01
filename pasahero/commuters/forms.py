from django import forms
from .models import Commuters
from cities.models import Cities
from transportations.models import Routes

class CommuterForm(forms.ModelForm):
    class Meta:
        model = Commuters
        exclude = ('id', 'user_id',)
        labels = {'lives_province_id':'Province', 
            'lives_city_id':'City',
            'works_province_id':'Province', 
            'works_city_id':'City',

            'first_name':'First Name',
            'last_name':'Last Name',
            'middle_name':'Middle Name',
            'profession':'Profession',
            'present_address':'Present Address',
            'permanent_address':'Permanent Address',
            'cell_number':'Cell Phone',
            'tele_number':'Telephone',
            'email':'Email',
            'preferred_pick_up':'Preferred Pick Up Location',
            'comments':'Important Facts',

            'company_name':'Company Name',
            'company_location':'Location',
            }

class EditCommuterForm(forms.ModelForm):
    class Meta:
        model = Commuters
        fields = ('email', 'cell_number', 'tele_number', 'preferred_pick_up', 'comments')
        labels = {'cell_number':'Cell Phone',
            'tele_number':'Telephone',
            'email':'Email',
            'preferred_pick_up':'Preferred Pick Up Location',
            'comments':'Important Facts',
            }

class FindRouteForm(forms.ModelForm):
    class Meta:
        model = Routes
        fields = ('province_id', 'city_id')
        labels = {'city_id':'City',
            'province_id':'Province',
            }
