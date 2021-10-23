from rest_framework.exceptions import ValidationError
from backend import settings
from .helpers import google_app_user_emails


class EmailValidationMixin:
    err_msg = {'email': 'Email must belong to the domain'}

    def email_check(self, validated_data):
        if settings.DEBUG:
            return

        if validated_data.get('is_staff') or validated_data.get('is_superuser'):
            if validated_data['email'] not in google_app_user_emails():
                raise ValidationError(self.err_msg)
