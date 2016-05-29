from edc_call_manager.model_caller import ModelCaller
from edc_call_manager.decorators import register

from tshipidi_plus.models import TshipidiSubject, SubjectLocator, SubjectConsent

from .models import Call, Log, LogEntry


@register(TshipidiSubject)
class TshipidiSubjectModelCaller(ModelCaller):
    call_model = (Call, 'tshipidi_subject')
    label = 'subjects'
    locator_model = (SubjectLocator, 'tshipidi_subject')
    log_entry_model = LogEntry
    log_model = Log
    unscheduling_model = SubjectConsent
