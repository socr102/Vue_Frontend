from django.core.management.base import BaseCommand, CommandError
from faker import Faker

import string
import random

from apps.members.models import Member
from backend.utils import positive_int, randomString

EXT_ID_CHOICES = string.ascii_lowercase + string.digits

class Command(BaseCommand):
    help = 'Populate database with fake members data'

    def add_arguments(self, parser):
        parser.add_argument('--orgId', type=positive_int, required=True, help='')
        parser.add_argument('--count', type=positive_int, required=True, help='')

    def handle(self, *args, **options):
        fake = Faker()
        members = []

        for i in range(options['count']):
            birth = fake.date_between(start_date='-70y', end_date='-15y')
            sex = Member.SEX_CHOICES[random.randint(0, 1)][0]
            if sex == Member.SEX_CHOICES[0][0]:
                name = fake.name_male()
            else:
                name = fake.name_female()

            members.append(Member(phone=fake.phone_number(),
                                  name=name,
                                  birth_date=birth,
                                  email=fake.email(),
                                  external_id=randomString(64, EXT_ID_CHOICES),
                                  organization_id=options['orgId'],
                                  sex=sex))

        Member.objects.bulk_create(members)
