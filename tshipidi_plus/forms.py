from django import forms
from .models import SubjectConsent


class SubjectConsentForm(forms.ModelForm):

    class Meta:
        model = SubjectConsent
        fields = '__all__'
