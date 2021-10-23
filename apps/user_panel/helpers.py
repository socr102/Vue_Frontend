from __future__ import print_function
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from django.conf import settings
from django.core.cache import cache

import os
from backend.settings import (SERVICE_ACCOUNT_EMAIL,
                              SERVICE_ACCOUNT_PKCS12_FILE_PATH,
                              SERVICE_ACCOUNT_PKCS12_FILE_PWD,
                              DELEGATED_EMAIL, DOMAIN)


def google_api_authenticate():
    p12_file = os.path.join(settings.BASE_DIR, SERVICE_ACCOUNT_PKCS12_FILE_PATH)
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL,
        p12_file,
        SERVICE_ACCOUNT_PKCS12_FILE_PWD,
        scopes=['https://www.googleapis.com/auth/admin.directory.user.readonly'])
    return credentials.create_delegated(DELEGATED_EMAIL)


def google_app_list_users(credentials):
    service = build('admin', 'directory_v1', credentials=credentials)
    users = service.users().list(domain=DOMAIN).execute()
    users = users.get('users', [])

    if users:
        return [user['primaryEmail'] for user in users]


def google_app_user_emails():
    cached_allowed_emails = cache.get('allowed_emails')
    if cached_allowed_emails:
        return cached_allowed_emails

    credentials = google_api_authenticate()
    allowed_emails = google_app_list_users(credentials)
    cache.set('allowed_emails', allowed_emails, 60)
    return allowed_emails
