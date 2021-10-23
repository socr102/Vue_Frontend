from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Create groups in database based on settings.py.'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name=settings.MERCHANT_ADMIN)
        Group.objects.get_or_create(name=settings.MERCHANT_WORKER)
