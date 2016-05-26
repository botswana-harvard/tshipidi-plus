from django.db import models
from django.core.exceptions import ValidationError
from django_crypto_fields.fields import IdentityField, FirstnameField, LastnameField, EncryptedCharField
from django.core.validators import RegexValidator

from simple_history.models import HistoricalRecords as AuditTrail

from edc_base.model.models import BaseUuidModel
from edc_call_manager.mixins import CallLogLocatorMixin
from edc_consent.models.base_consent import BaseConsent, ConsentManager, ObjectConsentManager
from edc_consent.models.fields import ReviewFieldsMixin, PersonalFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_constants.choices import GENDER
from edc_locator.models import LocatorMixin

from registration.models import RegisteredSubject


class SubjectConsent(BaseConsent, IdentityFieldsMixin, ReviewFieldsMixin,
                     PersonalFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    MIN_AGE_OF_CONSENT = 18
    MAX_AGE_OF_CONSENT = 64
    AGE_IS_ADULT = 18
    GENDER_OF_CONSENT = ['M', 'F']
    SUBJECT_TYPES = ['subject']

    history = AuditTrail()

    consent = ConsentManager()

    objects = ObjectConsentManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name, self.identity, self.subject_identifier)

    def save(self, *args, **kwargs):
        if not self.id:
            tshipidi_subject = self.fetch_tshipidi_subject(self.identity)
            self.subject_identifier = tshipidi_subject.subject_identifier
        super(SubjectConsent, self).save(*args, **kwargs)

    @classmethod
    def fetch_tshipidi_subject(cls, identity=None, exception_class=None):
        exception_class = exception_class or ValidationError
        try:
            tshipidi_subject = TshipidiSubject.objects.get(identity=identity)
        except TshipidiSubject.DoesNotExist:
            raise exception_class(
                'Tshipidi subject with identity \'{}\' was not found.'.format(identity))
        return tshipidi_subject

    class Meta:
        app_label = 'tshipidi_plus'
        get_latest_by = 'consent_datetime'
        unique_together = (('first_name', 'dob', 'initials', 'version'), )
        ordering = ('created', )


class TshipidiSubject(BaseUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject, null=True, editable=False)

    identity = IdentityField(
        verbose_name="Identity",
        unique=True,
        help_text=("Use Omang, Passport number, driver's license number or Omang receipt number")
    )

    subject_identifier = models.CharField(
        max_length=25,
        unique=True)

    first_name = FirstnameField(
        null=True,
    )

    last_name = LastnameField(
        verbose_name="Last name",
        null=True,
    )

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.')), ],
        null=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER,
        null=True)

    dob = models.DateField(null=True)

    subject_consent = models.ForeignKey(SubjectConsent, null=True, editable=False)

    contacted = models.BooleanField(default=False, editable=False)

    consented = models.BooleanField(default=False, editable=False)

    history = AuditTrail()

    def __str__(self):
        try:
            first_name = self.subject_consent.first_name
            last_name = self.subject_consent.last_name
            name = first_name + ' ' + last_name
        except AttributeError:
            name = 'not consented'
        return '{}. {}'.format(
            name, self.subject_identifier)

    class Meta:
        app_label = 'tshipidi_plus'


class SubjectLocator(LocatorMixin, CallLogLocatorMixin, BaseUuidModel):

    tshipidi_subject = models.ForeignKey(TshipidiSubject)

    history = AuditTrail()

    def get_call_log_options(self):
        return dict(call__tshipidi_subject=self.tshipidi_subject)

    class Meta:
        app_label = 'tshipidi_plus'
