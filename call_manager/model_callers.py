from edc_call_manager.model_caller import ModelCaller
from edc_call_manager.decorators import register

from tshipidi_plus.models import TshipidiSubject, SubjectLocator, SubjectConsent
from call_manager.models import Call, Log, LogEntry


@register(TshipidiSubject)
class TshipidiSubjectModelCaller(ModelCaller):
    label = 'subjects'
    locator_model = (SubjectLocator, 'tshipidi_subject__subject_identifier')
    call_model = (Call, 'tshipidi_subject')
    log_model = Log
    log_entry_model = LogEntry
    unscheduling_model = SubjectConsent
