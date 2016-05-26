import csv
import os
import random
from faker import Faker
from faker.providers import BaseProvider

from django.core.management.base import BaseCommand, CommandError
from tshipidi_plus.models import TshipidiSubject, SubjectLocator
from edc_identifier.subject.classes.subject_identifier import SubjectIdentifier
from edc_constants.constants import YES, NO

fake = Faker()


class BwCellProvider(BaseProvider):
    def cellphonebw(self):
        return '7' + str(random.randint(1000000, 9999999))

fake.add_provider(BwCellProvider)


class Command(BaseCommand):

    help = 'Load test data. Defaults to create TshipidiSubjects.'

    def add_arguments(self, parser):
        parser.add_argument('-f', nargs='?', type=str, help='csv filename prefix (two files will be created')
        parser.add_argument('-n', nargs='?', type=int, help='number of records to create')

    def handle(self, *args, **options):
        self.tshipidi_subjects = []
        self.subject_locators = []
        csv_filename = options.get('f')
        self.csv_filenames = {}
        records = options.get('n')
        records = records or 150
        if not csv_filename:
            if TshipidiSubject.objects.all().count() > 0:
                raise CommandError('TshipidiSubjects is already populated. Cannot load test data.')
        else:
            csv_filename = csv_filename.split('.')[0]
            self.csv_filenames = {
                'subject_locators': '{}_subject_locators.csv'.format(csv_filename),
                'tshipidi_subjects': '{}_tshipidi_subjects.csv'.format(csv_filename),
            }
        self.stdout.write(self.style.SUCCESS(
            'Adding {} records of test data'.format(records)))
        index = 0
        while index <= records:
            print(index, end='\r')
            index += 1
            tshipidi_subject = self.create_tshipidi_subject()
            self.create_subject_locator(tshipidi_subject=tshipidi_subject)
        if csv_filename:
            self.write_tshipidi_subjects()
            self.write_subject_locators()
        self.stdout.write(self.style.SUCCESS('Done'))

    def write_tshipidi_subjects(self):
        fieldnames = ['subject_identifier', 'first_name', 'last_name', 'identity',
                      'initials', 'dob', 'gender', 'category', 'sub_category', 'community']
        with open(os.path.expanduser('~/{}'.format(self.csv_filenames['tshipidi_subjects'])), 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.tshipidi_subjects)

    def write_subject_locators(self):
        fieldnames = list(self.subject_locators[0].keys())
        with open(os.path.expanduser('~/{}'.format(self.csv_filenames['subject_locators'])), 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.subject_locators)

    def create_subject_locator(self, tshipidi_subject):
        options = dict(
            tshipidi_subject=tshipidi_subject,
            home_visit_permission=YES,
            physical_address=fake.address(),
            may_follow_up=YES,
            subject_cell=fake.cellphonebw(),
            subject_cell_alt=fake.cellphonebw(),
            may_call_work=random.choice([YES, NO]),
            may_contact_someone=random.choice([YES, NO]),
        )
        if options['may_contact_someone'] == YES:
            options.update(contact_name=fake.name())
            options.update(contact_cell=fake.cellphonebw())
        else:
            options.update(contact_name=None)
            options.update(contact_cell=None)
        if self.csv_filenames:
            self.subject_locators.append(options)
        else:
            SubjectLocator.objects.create(**options)

    def create_tshipidi_subject(self):
        gender = random.choice(['M', 'F'])
        if gender == 'F':
            first_name, last_name = fake.first_name_female(), fake.last_name_female()
        else:
            first_name, last_name = fake.first_name_male(), fake.last_name_male()
        subject_identifier = SubjectIdentifier(site_code='99').get_identifier(add_check_digit=True)
        profile = fake.profile()
        birthdate = profile['birthdate']
        omang = ''.join(profile['ssn'].split('-'))
        omang = '{}{}{}'.format(omang[0:4], 1 if gender == 'M' else 2, omang[5:])
        options = dict(
            first_name=first_name,
            last_name=last_name,
            dob=birthdate,
            identity=omang,
            subject_identifier=subject_identifier,
            initials=first_name[0].upper() + last_name[0].upper(),
            gender=gender)
        if self.csv_filenames:
            self.tshipidi_subjects.append(options)
            tshipidi_subject = options['subject_identifier']
        else:
            tshipidi_subject = TshipidiSubject.objects.create(**options)
        return tshipidi_subject
