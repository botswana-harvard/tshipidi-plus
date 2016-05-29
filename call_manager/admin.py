from django.contrib import admin
from django.contrib.admin.options import StackedInline

from simple_history.admin import SimpleHistoryAdmin

from edc_base.modeladmin.mixins import (
    ModelAdminAuditFieldsMixin,
    ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin, ModelAdminModelRedirectMixin,
    # ModelAdminChangelistModelButtonMixin,
    ModelAdminChangelistButtonMixin)
from edc_call_manager.admin import (
    ModelAdminCallMixin, ModelAdminLogMixin, ModelAdminLogEntryMixin,
    ModelAdminLogEntryInlineMixin, call_manager_admin)
from edc_constants.constants import NEW, OPEN

from .models import Call, Log, LogEntry


class BaseModelAdmin(ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class ModelAdminStackedInlineMixin(ModelAdminAuditFieldsMixin, StackedInline):
    pass


@admin.register(Call, site=call_manager_admin)
class CallAdmin(BaseModelAdmin, ModelAdminCallMixin,
                ModelAdminChangelistButtonMixin,
                # ModelAdminChangelistModelButtonMixin,
                SimpleHistoryAdmin):

    mixin_list_display = None

    list_display = (
        'subject_identifier',
        'call_button',
        'call_attempts',
        'call_outcome',
        'scheduled',
        'label',
        'first_name',
        'initials',
        'user_created',
    )

    def call_button(self, obj):
        log = Log.objects.get(call=obj)
        if obj.call_status == NEW:
            change_label = 'New&nbsp;Call'.format(obj.call_attempts)
        elif obj.call_status == OPEN:
            change_label = 'Open&nbsp;Call'.format(obj.call_attempts)
        else:
            change_label = 'Closed&nbsp;Call'
        return self.change_button(
            'call-subject-add', ('tshipidi_plus', 'tshipidisubject', str(log.pk), ),
            label=change_label, namespace='call_manager')
    call_button.short_description = 'call'

#     def call_button(self, obj):
#         log = Log.objects.get(call=obj)
#         if obj.call_status == NEW:
#             change_label = 'Call'.format(obj.call_attempts)
#         elif obj.call_status == OPEN:
#             change_label = 'Call'.format(obj.call_attempts)
#         else:
#             return 'Closed'
#         return self.changelist_model_button(
#             'call_manager', 'log', (log.pk, ), namespace='call_manager_admin',
#             change_label=change_label)
#     call_button.short_description = 'call'


class LogEntryInlineAdmin(ModelAdminLogEntryInlineMixin, ModelAdminStackedInlineMixin):

    model = LogEntry


@admin.register(Log, site=call_manager_admin)
class LogAdmin(BaseModelAdmin, ModelAdminModelRedirectMixin, ModelAdminLogMixin, SimpleHistoryAdmin):

    redirect_app_label = 'call_manager'
    redirect_model_name = 'call'
    redirect_search_field = 'call__subject_identifier'
    redirect_namespace = 'call_manager_admin'

    inlines = [LogEntryInlineAdmin]

    readonly_fields = ('call', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "call":
            try:
                call = Call.objects.get(pk=request.GET.get('call'))
                kwargs["queryset"] = [call]
            except Call.DoesNotExist:
                pass
        return super(LogAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(LogEntry, site=call_manager_admin)
class LogEntryAdmin(BaseModelAdmin, ModelAdminLogEntryMixin, SimpleHistoryAdmin):
    pass
