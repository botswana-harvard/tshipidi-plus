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

    redirect_app_label = 'bcpp_interview'
    redirect_model_name = 'tshipidisubject'


@admin.register(RegisteredSubject, site=registration_admin)
class RegisteredSubjectAdmin(RegisteredSubjectModelAdminMixin, BaseModelAdmin):
    pass


@admin.register(SubjectLocator)
class SubjectLocatorAdmin(ModelAdminLocatorMixin, BaseModelAdmin):

    fields = ['tshipidi_subject']

    readonly_fields = ('tshipidi_subject', )

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
