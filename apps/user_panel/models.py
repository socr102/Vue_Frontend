from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.functional import cached_property

from .managers import CustomUserManager
from apps.organizations.models import Organization


class CustomUser(AbstractUser):
    CONTACT_CHOICES = (
        ("EM", "Email"),
        ("PC", "Phone Call"),
        ("SS", "SMS"),
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    delete_request = models.ForeignKey('self', models.SET_NULL, default=None, null=True, blank=True)
    created_by = models.ForeignKey('CustomUser',
                                   related_name='creator',
                                   on_delete=models.CASCADE,
                                   default=None, null=True,
                                   blank=True)

    social_security = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    allow_contact = models.BooleanField(default=True)
    contact_way = models.CharField(max_length=10,
                                   choices=CONTACT_CHOICES,
                                   default="EM")

    organization = models.ForeignKey(Organization,
                                     models.SET_NULL,
                                     default=None,
                                     null=True,
                                     blank=True)

    def __str__(self):
        return self.email

    @cached_property
    def is_merchant(self):
        return self.groups.filter(name=settings.MERCHANT_ADMIN).exists()
