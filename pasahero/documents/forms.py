from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import Documents

class CreateDocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('title', 'description', 'document')

class UpdateDocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('title', 'description')

