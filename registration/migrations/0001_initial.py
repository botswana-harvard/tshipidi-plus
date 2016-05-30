# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 05:57
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_crypto_fields.fields.encrypted_char_field
import django_crypto_fields.fields.firstname_field
import django_crypto_fields.fields.identity_field
import django_crypto_fields.fields.lastname_field
import django_extensions.db.fields
import django_revision.revision_field
import edc_base.model.fields.custom_fields
import edc_base.model.fields.hostname_modification_field
import edc_base.model.fields.userfield
import edc_base.model.fields.uuid_auto_field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRegisteredSubject',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(db_index=True, editable=False, help_text='System field. UUID primary key.')),
                ('subject_identifier', models.CharField(blank=True, db_index=True, max_length=50, verbose_name='Subject Identifier')),
                ('subject_identifier_as_pk', models.CharField(db_index=True, max_length=50, null=True, verbose_name='Subject Identifier as pk')),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('last_name', django_crypto_fields.fields.lastname_field.LastnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='Last name')),
                ('initials', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(help_text=' (Encryption: RSA local)', max_length=71, null=True, validators=[django.core.validators.RegexValidator(message='Ensure initials consist of letters only in upper case, no spaces.', regex='^[A-Z]{2,3}$')])),
                ('dob', models.DateField(help_text='Format is YYYY-MM-DD', null=True, verbose_name='Date of birth')),
                ('is_dob_estimated', edc_base.model.fields.custom_fields.IsDateEstimatedField(choices=[('-', 'No'), ('D', 'Yes, estimated the Day'), ('MD', 'Yes, estimated Month and Day'), ('YMD', 'Yes, estimated Year, Month and Day')], help_text='If the exact date is not known, please indicate which part of the date is estimated.', max_length=25, null=True, verbose_name='Is date of birth estimated?')),
                ('gender', models.CharField(max_length=1, null=True, verbose_name='Gender')),
                ('subject_type', models.CharField(max_length=25)),
                ('subject_consent_id', models.CharField(blank=True, max_length=100, null=True)),
                ('registration_identifier', models.CharField(blank=True, max_length=36, null=True)),
                ('sid', models.CharField(blank=True, max_length=15, null=True, verbose_name='SID')),
                ('study_site', models.CharField(blank=True, max_length=50, null=True)),
                ('relative_identifier', models.CharField(blank=True, help_text="For example, mother's identifier, if available / appropriate", max_length=25, null=True, verbose_name='Identifier of immediate relation')),
                ('identity', django_crypto_fields.fields.identity_field.IdentityField(blank=True, help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('identity_type', edc_base.model.fields.custom_fields.IdentityTypeField(choices=[('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other')], max_length=15, verbose_name='What type of identity number is this?')),
                ('may_store_samples', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='?', help_text='Does the subject agree to have samples stored after the study has ended', max_length=3, verbose_name='Sample storage')),
                ('hiv_status', models.CharField(blank=True, choices=[('POS', 'Positive'), ('NEG', 'Negative'), ('unknown', 'Unknown')], max_length=15, null=True, verbose_name='Hiv status')),
                ('survival_status', models.CharField(blank=True, choices=[('alive', 'Alive'), ('dead', 'Dead'), ('unknown', 'Unknown')], max_length=15, null=True, verbose_name='Survival status')),
                ('screening_identifier', models.CharField(blank=True, max_length=36, null=True)),
                ('screening_datetime', models.DateTimeField(blank=True, null=True)),
                ('screening_age_in_years', models.IntegerField(blank=True, null=True)),
                ('registration_datetime', models.DateTimeField(blank=True, null=True)),
                ('randomization_datetime', models.DateTimeField(blank=True, null=True)),
                ('registration_status', models.CharField(blank=True, max_length=25, null=True, verbose_name='Registration status')),
                ('comment', models.TextField(blank=True, max_length=250, null=True, verbose_name='Comment')),
                ('additional_key', models.CharField(default=None, editable=False, help_text='A uuid (or some other text value) to be added to bypass the unique constraint of just firstname, initials, and dob.The default constraint proves limiting since the source model usually has some otherattribute in additional to first_name, initials and dob which is not captured in this model', max_length=36, null=True, verbose_name='-')),
                ('dm_comment', models.CharField(editable=False, max_length=150, null=True, verbose_name='Data Management comment')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical registered subject',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='RegisteredSubject',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(editable=False, max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(default='mac2-2.local', editable=False, help_text='System field. (modified on create only)', max_length=50)),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(editable=False, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(editable=False, help_text='System field. UUID primary key.', primary_key=True, serialize=False)),
                ('subject_identifier', models.CharField(blank=True, db_index=True, max_length=50, unique=True, verbose_name='Subject Identifier')),
                ('subject_identifier_as_pk', models.CharField(db_index=True, max_length=50, null=True, verbose_name='Subject Identifier as pk')),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('first_name', django_crypto_fields.fields.firstname_field.FirstnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('last_name', django_crypto_fields.fields.lastname_field.LastnameField(help_text=' (Encryption: RSA local)', max_length=71, null=True, verbose_name='Last name')),
                ('initials', django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(help_text=' (Encryption: RSA local)', max_length=71, null=True, validators=[django.core.validators.RegexValidator(message='Ensure initials consist of letters only in upper case, no spaces.', regex='^[A-Z]{2,3}$')])),
                ('dob', models.DateField(help_text='Format is YYYY-MM-DD', null=True, verbose_name='Date of birth')),
                ('is_dob_estimated', edc_base.model.fields.custom_fields.IsDateEstimatedField(choices=[('-', 'No'), ('D', 'Yes, estimated the Day'), ('MD', 'Yes, estimated Month and Day'), ('YMD', 'Yes, estimated Year, Month and Day')], help_text='If the exact date is not known, please indicate which part of the date is estimated.', max_length=25, null=True, verbose_name='Is date of birth estimated?')),
                ('gender', models.CharField(max_length=1, null=True, verbose_name='Gender')),
                ('subject_type', models.CharField(max_length=25)),
                ('subject_consent_id', models.CharField(blank=True, max_length=100, null=True)),
                ('registration_identifier', models.CharField(blank=True, max_length=36, null=True)),
                ('sid', models.CharField(blank=True, max_length=15, null=True, verbose_name='SID')),
                ('study_site', models.CharField(blank=True, max_length=50, null=True)),
                ('relative_identifier', models.CharField(blank=True, help_text="For example, mother's identifier, if available / appropriate", max_length=25, null=True, verbose_name='Identifier of immediate relation')),
                ('identity', django_crypto_fields.fields.identity_field.IdentityField(blank=True, help_text=' (Encryption: RSA local)', max_length=71, null=True)),
                ('identity_type', edc_base.model.fields.custom_fields.IdentityTypeField(choices=[('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other')], max_length=15, verbose_name='What type of identity number is this?')),
                ('may_store_samples', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='?', help_text='Does the subject agree to have samples stored after the study has ended', max_length=3, verbose_name='Sample storage')),
                ('hiv_status', models.CharField(blank=True, choices=[('POS', 'Positive'), ('NEG', 'Negative'), ('unknown', 'Unknown')], max_length=15, null=True, verbose_name='Hiv status')),
                ('survival_status', models.CharField(blank=True, choices=[('alive', 'Alive'), ('dead', 'Dead'), ('unknown', 'Unknown')], max_length=15, null=True, verbose_name='Survival status')),
                ('screening_identifier', models.CharField(blank=True, max_length=36, null=True)),
                ('screening_datetime', models.DateTimeField(blank=True, null=True)),
                ('screening_age_in_years', models.IntegerField(blank=True, null=True)),
                ('registration_datetime', models.DateTimeField(blank=True, null=True)),
                ('randomization_datetime', models.DateTimeField(blank=True, null=True)),
                ('registration_status', models.CharField(blank=True, max_length=25, null=True, verbose_name='Registration status')),
                ('comment', models.TextField(blank=True, max_length=250, null=True, verbose_name='Comment')),
                ('additional_key', models.CharField(default=None, editable=False, help_text='A uuid (or some other text value) to be added to bypass the unique constraint of just firstname, initials, and dob.The default constraint proves limiting since the source model usually has some otherattribute in additional to first_name, initials and dob which is not captured in this model', max_length=36, null=True, verbose_name='-')),
                ('dm_comment', models.CharField(editable=False, max_length=150, null=True, verbose_name='Data Management comment')),
            ],
        ),
    ]
