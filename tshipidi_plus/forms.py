from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import TshipidiSubject, SubjectConsent


class SubjectConsentForm(forms.ModelForm):

    class Meta:
        model = SubjectConsent
        fields = '__all__'


class TshipidiSubjectForm(forms.ModelForm):

    class Meta:
        model = TshipidiSubject
        fields = '__all__'


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
