from django.contrib import admin
from django.contrib.admin.options import TabularInline

from edc_base.modeladmin.mixins import (
    ModelAdminModelRedirectMixin, ModelAdminChangelistModelButtonMixin,
    ModelAdminRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin)
from edc_consent.admin.mixins import ModelAdminConsentMixin
from edc_locator.admin import ModelAdminLocatorMixin
from edc_registration.admin import RegisteredSubjectModelAdminMixin, registration_admin

from simple_history.admin import SimpleHistoryAdmin
from registration.models import RegisteredSubject

from .forms import SubjectConsentForm
from .models import SubjectConsent, SubjectLocator, TshipidiSubject


class BaseModelAdminTabularInline(ModelAdminAuditFieldsMixin, TabularInline):
    pass


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
                     ModelAdminAuditFieldsMixin, SimpleHistoryAdmin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class ModelAdminTshipidiSubjectRedirectMixin(ModelAdminModelRedirectMixin):

    redirect_app_label = 'tshipidi_plus'
    redirect_model_name = 'tshipidisubject'


@admin.register(RegisteredSubject, site=registration_admin)
class RegisteredSubjectAdmin(RegisteredSubjectModelAdminMixin, BaseModelAdmin):
    pass


@admin.register(TshipidiSubject)
class TshipidiSubjectAdmin(ModelAdminChangelistModelButtonMixin, BaseModelAdmin):

    list_display = ['subject_identifier', 'identity', 'consent_button', 'subject_status']

    list_filter = ['contacted', 'consented']

    search_fields = ['identity', 'subject_identifier', 'registered_subject__identity']

    readonly_fields = ['subject_identifier', 'identity']

    def subject_status(self, obj):
        template = '<span>{contacted}&nbsp;&nbsp;{consented}&nbsp;&nbsp;{interviewed}</span>'
        contacted, consented, interviewed = [''] * 3
        if obj.contacted:
            contacted = '<i class="fa fa-phone fa-1x" title="Contacted" aria-hidden="true"></i>'
            if obj.consented:
                consented = '<i class="fa fa-file-text fa-1x" title="Consented" aria-hidden="true"></i>'
        return template.format(contacted=contacted, consented=consented, interviewed=interviewed)
    subject_status.short_dscription = 'subject status'
    subject_status.allow_tags = True

    def consent_button(self, obj):
        reverse_args = None
        if obj.subject_consent:
            reverse_args = (obj.subject_consent.pk, )
        return self.changelist_model_button(
            'tshipidi_plus', 'subjectconsent', reverse_args=reverse_args,
            change_label='consent')
    consent_button.short_description = 'Consent'


@admin.register(SubjectLocator)
class SubjectLocatorAdmin(ModelAdminLocatorMixin, ModelAdminTshipidiSubjectRedirectMixin, BaseModelAdmin):

    fields = ['tshipidi_subject']

    readonly_fields = ('tshipidi_subject', )

    redirect_search_field = 'tshipidi_subject__subject_identifier'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tshipidi_subject":
            try:
                tshipidi_subject = TshipidiSubject.objects.get(pk=request.GET.get('tshipidi_subject'))
                kwargs["queryset"] = [tshipidi_subject]
            except TshipidiSubject.DoesNotExist:
                pass
        return super(SubjectLocatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(SubjectConsent)
class SubjectConsentAdmin(ModelAdminConsentMixin,
                          ModelAdminTshipidiSubjectRedirectMixin, BaseModelAdmin):

    additional_instructions = 'After saving you will be returned to the list of Tshipidi Subjects.'

    mixin_exclude_fields = ['may_store_samples', 'study_site']

    redirect_search_field = 'subject_identifier'

    form = SubjectConsentForm
