import pytest
import json
from django.test import TestCase
from rest_framework.test import APIClient

from user_panel.tests.helpers import generate_user, create_merchant_by_admin, superuser_create_user


class TestAdminApiView(TestCase):
    def setUp(self) -> None:
        self.admin = superuser_create_user(True)
        self.admin_client = APIClient()
        self.admin['access'] = self.admin_client.post('/api/v1/token/',
                                                      content_type='application/json',
                                                      data=json.dumps({'email': self.admin['email'],
                                                                       'password': self.admin['password']
                                                                       })).data['access']
        self.admin_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin['access'])

    def test_admin_list_accounts(self):
        response = self.admin_client.get('/api/v1/account/')
        assert response.status_code == 200

        response_data = response.json()
        assert isinstance(response_data, list)

        assert self.admin['email'] in [item['email'] for item in response_data]

    def test_admin_create_merchant(self):
        merchant = generate_user()
        response = self.admin_client.post('/api/v1/account/', content_type='application/json',
                                          data=json.dumps({'email': merchant['email'],
                                                           'password': merchant['password'],
                                                           'is_merchant': True}))
        assert response.status_code == 201

        response_data = response.json()
        assert list(response_data.keys()) == ['email', 'id', 'is_staff', 'is_superuser', 'is_active',
                                              'delete_request', 'created_by', 'is_merchant']
        assert response_data['email'] == merchant['email']
        assert response_data['is_merchant']
        assert response_data['created_by'] == {'email': self.admin['email'], 'id': self.admin['id']}

    def test_admin_list_users(self):
        merchant = create_merchant_by_admin(self.admin_client)
        response = self.admin_client.get("/api/v1/account/").json()

        assert merchant['email'] in [r['email'] for r in response]
        for r in response:
            if r['email'] == merchant['email']:
                assert r == {'email': merchant['email'],
                             'id': merchant['user_id'],
                             'is_staff': False,
                             'is_superuser': False,
                             'is_active': True,
                             'is_merchant': True,
                             'delete_request': None,
                             'created_by': {'id': self.admin['id'],
                                            'email': self.admin['email']}}

    def test_admin_detail_merchant(self):
        merchant = create_merchant_by_admin(self.admin_client)
        response = self.admin_client.get(f"/api/v1/account/{merchant['user_id']}/").json()

        assert response == {'id': response['id'],
                            'email': merchant['email'],
                            'first_name': '',
                            'last_name': '',
                            'is_staff': merchant['is_staff'],
                            'delete_request': None,
                            'social_security': '',
                            'is_active': True,
                            'is_merchant': True,
                            'phone': '',
                            'allow_contact': True,
                            'contact_way': 'EM',
                            'is_superuser': False,
                            'created_by': {'id': self.admin['id'], 'email': self.admin['email']}}

    def test_admin_update_user(self):
        user = create_merchant_by_admin(self.admin_client)
        self.admin_client.patch(f"/api/v1/account/{user['user_id']}/", data=user).json()

        response = self.admin_client.get(f"/api/v1/account/{user['user_id']}/").json()
        assert response == {'id': response['id'],
                            'email': user['email'],
                            'first_name': user['first_name'],
                            'last_name': user['last_name'],
                            'is_staff': user['is_staff'],
                            'delete_request': None,
                            'social_security': str(user['social_security']),
                            'phone': str(user['phone']),
                            'is_active': True,
                            'allow_contact': True,
                            'is_merchant': True,
                            'contact_way': user['contact_way'],
                            'is_superuser': False,
                            'created_by': {'id': self.admin['id'], 'email': self.admin['email']}}

    def test_admin_delete_user(self):
        user = create_merchant_by_admin(self.admin_client)
        response = self.admin_client.delete(f"/api/v1/account/{user['user_id']}/")

        assert response.status_code == 200
        assert not response.data['delete_request']

    def test_negative_admin_create_superuser(self):
        user = generate_user()
        response = self.admin_client.post('/api/v1/account/', content_type='application/json',
                                          data=json.dumps({'email': user['email'],
                                                           'password': user['password'],
                                                           'is_superuser': True}))
        assert response.status_code == 403

    def test_negative_admin_update_to_superuser(self):
        user = create_merchant_by_admin(self.admin_client)
        user['is_superuser'] = True
        response = self.admin_client.patch(f"/api/v1/account/{user['user_id']}/", data=user).json()

        assert response == {'detail': 'You cant update is_superuser field'}

    def test_negative_admin_delete_superuser(self):
        pass

    def test_negative_admin_delete_user(self):
        pass

    def test_negative_admin_update_superuser(self):
        pass

    def test_negative_admin_create_worker(self):
        pass
