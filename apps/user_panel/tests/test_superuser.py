import pytest
import json
from django.test import TestCase
from rest_framework.test import APIClient

from backend.settings import SUPERUSER_DATA, DEBUG

from user_panel.tests.helpers import generate_user


class TestSuperuserApiView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.SUPERUSER = self.client.post('/api/v1/token/', data=SUPERUSER_DATA).data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.SUPERUSER['access'])

    def test_superuser_list_accounts(self):
        response = self.client.get('/api/v1/account/')
        assert response.status_code == 200

        response_data = response.json()
        assert isinstance(response_data, list)
        assert isinstance(response_data[0], dict)

        users = [item['email'] for item in response_data]
        assert SUPERUSER_DATA['email'] in users

    @pytest.mark.foo
    def test_superuser_create_admin(self):
        admin = generate_user(True)
        response = self.client.post('/api/v1/account/', data=admin)
        assert response.status_code == 201

        response_data = response.json()
        assert response_data == {'created_by': {'email': 'superuser@gmail.com', 'id': self.SUPERUSER['id']},
                                 'email': admin['email'],
                                 'id': response_data['id'],
                                 'is_staff': True,
                                 'is_superuser': False,
                                 'is_active': True,
                                 'delete_request': None,
                                 'organization': None}

    def test_superuser_detail_admin(self):
        merchant = generate_user(True)
        # merchant['group_id'] = 1
        merchant_id = self.client.post('/api/v1/account/', data=merchant).json()['id']

        response = self.client.get(f'/api/v1/account/{merchant_id}/').json()
        response_data = response.json()
        assert response_data == {'email': merchant['email'],
                                 'id': response_data['id'],
                                 'is_staff': False,
                                 'is_superuser': False,
                                 'is_active': True,
                                 'delete_request': None,
                                 'organization': None,
                                 'created_by': {'id': 1, 'email': 'superuser@gmail.com'},
                                 }

    @pytest.mark.foo
    def test_superuser_create_merchant(self):
        merchant = generate_user()
        merchant['groups'] = [3]
        response = self.client.post('/api/v1/account/', data=merchant)
        assert response.status_code == 201

        response_data = response.json()
        assert response_data == {'email': merchant['email'],
                                 'id': response_data['id'],
                                 'is_staff': False,
                                 'is_superuser': False,
                                 'is_active': True,
                                 'delete_request': None,
                                 'groups': [3],
                                 'organization': None,
                                 'created_by': {'id': 1, 'email': 'superuser@gmail.com'},
                                 }

    def test_superuser_detail_merchant(self):
        merchant = generate_user()
        merchant_id = self.client.post('/api/v1/account/', data=merchant).json()['id']

        response_data = self.client.get(f'/api/v1/account/{merchant_id}/').json()
        assert response_data == {'email': merchant['email'],
                                 'id': response_data['id'],
                                 'is_staff': False,
                                 'is_superuser': False,
                                 'is_active': True,
                                 'delete_request': None,
                                 'is_merchant': True,
                                 'first_name': '',
                                 'last_name': '',
                                 'organization': None,
                                 'phone': '',
                                 'social_security': '',
                                 'allow_contact': True,
                                 'contact_way': 'EM',
                                 'created_by': {'id': 1, 'email': 'superuser@gmail.com'},
                                 }

    def test_superuser_update_merchant(self):
        merchant = generate_user()
        user_id = self.client.post('/api/v1/account/', data=merchant).json()['id']
        self.client.patch(f'/api/v1/account/{user_id}/', data=merchant).json()

        response_data = self.client.get(f'/api/v1/account/{user_id}/').json()

        assert response_data == {'email': merchant['email'],
                                 'id': response_data['id'],
                                 'is_staff': False,
                                 'is_superuser': False,
                                 'is_active': True,
                                 'delete_request': None,
                                 'is_merchant': True,
                                 'first_name': merchant['first_name'],
                                 'last_name': merchant['last_name'],
                                 'organization': None,
                                 'phone': str(merchant['phone']),
                                 'social_security': str(merchant['social_security']),
                                 'allow_contact': True,
                                 'contact_way': 'EM',
                                 'created_by': {'id': 1, 'email': 'superuser@gmail.com'},
                                 }

    def test_superuser_delete_merchant(self):
        user = generate_user()
        user_id = self.client.post('/api/v1/account/', data=user).json()['id']
        response = self.client.delete(f'/api/v1/account/{user_id}/')

        assert response.status_code == 204

        response = self.client.get('/api/v1/account/').json()
        assert user['email'] not in [user['email'] for user in response]

    def test_negative_create_user(self):
        if DEBUG:
            return
        response = self.client.post('/api/v1/account/', content_type='application/json',
                                    data=json.dumps({'email': 'email@invalid.domain', 'password': 'password'}))
        assert response.status_code == 400
        assert response.json() == {'detail': 'Mail must belong to the domain'}
