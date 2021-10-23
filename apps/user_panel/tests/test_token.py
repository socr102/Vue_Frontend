import pytest
import json
from django.test import TestCase
from rest_framework.test import APIClient

from backend.settings import SUPERUSER_DATA
from user_panel.tests.helpers import generate_user


class TestGetToken(TestCase):
    """
    Test get tokens for different user types [superuser, admin, merchant, worker]
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = generate_user(True)
        self.user = generate_user()

    def test_get_superuser_token(self):
        response = self.client.post('/api/v1/token/', data=SUPERUSER_DATA)
        assert response.status_code == 200
        result = response.json()
        assert ['refresh', 'access', 'id'] == list(result.keys())

    def test_get_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.client.post('/api/v1/token/',
                                                                                data=SUPERUSER_DATA).data['access'])
        self.client.post('/api/v1/account/',
                         content_type='application/json',
                         data=json.dumps({'email': self.admin['email'],
                                          'password': self.admin['password'],
                                          'is_staff': True}))
        response = self.client.post('/api/v1/token/',
                                    content_type='application/json',
                                    data=json.dumps({'email': self.admin['email'],
                                                     'password': self.admin['password']}))
        assert response.status_code == 200
        result = response.json()
        assert ['refresh', 'access', 'id'] == list(result.keys())

    def test_get_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.client.post('/api/v1/token/',
                                                                                data=SUPERUSER_DATA).data['access'])
        self.client.post('/api/v1/account/',
                         content_type='application/json',
                         data=json.dumps({'email': self.user['email'],
                                          'password': self.user['password'],
                                          'is_staff': False}))
        response = self.client.post('/api/v1/token/', content_type='application/json',
                                    data=json.dumps({'email': self.user['email'], 'password': self.user['password']}))
        assert response.status_code == 200
        result = response.json()
        assert ['refresh', 'access', 'id'] == list(result.keys())
