from django import forms
from call_manager.models import LogEntry
from edc_call_manager.forms import LogEntryFormMixin
from tshipidi_plus.models import TshipidiSubject


class LogEntryForm(LogEntryFormMixin, forms.ModelForm):

    class Meta(LogEntryFormMixin.Meta):
        model = LogEntry
        fields = '__all__'


class TshipidiSubjectForm(forms.ModelForm):

    class Meta:
        model = TshipidiSubject
        fields = '__all__'
