import pytest
import json
from django.test import TestCase
from rest_framework.test import APIClient

from user_panel.tests.helpers import generate_user, superuser_create_user, create_worker_by_merchant


class TestMerchantApiView(TestCase):
    def setUp(self) -> None:
        self.merchant = superuser_create_user(False)
        self.merchant['created_by'] = {'id': 1, 'email': 'superuser@gmail.com'}
        self.merchant_client = APIClient()
        self.merchant['access'] = self.merchant_client.post('/api/v1/token/',
                                                            content_type='application/json',
                                                            data=json.dumps({'email': self.merchant['email'],
                                                                             'password': self.merchant['password']
                                                                             })).data['access']
        self.merchant_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.merchant['access'])

    def test_merchant_detail_self(self):
        response = self.merchant_client.get(f"/api/v1/account/{self.merchant['id']}/").json()

        assert response == {'id': response['id'],
                            'email': self.merchant['email'],
                            'first_name': '',
                            'last_name': '',
                            'is_staff': self.merchant['is_staff'],
                            'delete_request': None,
                            'social_security': '',
                            'is_active': True,
                            'phone': '',
                            'allow_contact': True,
                            'contact_way': 'EM',
                            'is_superuser': False,
                            'is_merchant': True,
                            'organization': None,
                            'created_by': self.merchant['created_by']}

    def test_merchant_update_self(self):
        new_merchant_data = generate_user(admin=False)
        self.merchant_client.patch(f"/api/v1/account/{self.merchant['id']}/", data=new_merchant_data).json()

        response = self.merchant_client.get(f"/api/v1/account/{self.merchant['id']}/").json()
        assert response == {'id': self.merchant['id'],
                            'email': new_merchant_data['email'],
                            'first_name': new_merchant_data['first_name'],
                            'last_name': new_merchant_data['last_name'],
                            'delete_request': None,
                            'social_security': str(new_merchant_data['social_security']),
                            'phone': str(new_merchant_data['phone']),
                            'is_active': True,
                            'allow_contact': True,
                            'contact_way': new_merchant_data['contact_way'],
                            'is_superuser': False,
                            'is_staff': False,
                            'is_merchant': True,
                            'created_by': self.merchant['created_by']}

    @pytest.mark.skip
    def test_merchant_delete_self(self):
        pass
        # user = create_user_by_merchant(self.merchant_client)
        # response = self.merchant_client.delete(f"/api/v1/account/{user['user_id']}/")
        #
        # assert response.status_code == 200
        # assert not response.data['delete_request']

    def test_merchant_create_worker(self):
        worker = generate_user()
        worker['is_worker'] = True
        response = self.merchant_client.post('/api/v1/account/', content_type='application/json',
                                             data=json.dumps({'email': worker['email'],
                                                              'password': worker['password'],
                                                              'is_worker': True}))
        assert response.status_code == 201

        response_data = response.json()
        assert response_data == {'email': worker['email'],
                                 'id': response_data['id'],
                                 'is_staff': False,
                                 'is_superuser': False,
                                 'is_active': True,
                                 'delete_request': None,
                                 'is_merchant': False,
                                 'organization': None,
                                 'created_by': {'id': self.merchant['id'], 'email': self.merchant['email']},
                                 }

    @pytest.mark.foo
    def test_merchant_list_workers(self):
        worker = create_worker_by_merchant(self.merchant_client)
        response = self.merchant_client.get("/api/v1/account/").json()

        assert worker['email'] in [r['email'] for r in response]
        for r in response:
            if r['email'] == worker['email']:
                assert r == {'email': worker['email'],
                             'id': worker['user_id'],
                             'is_staff': False,
                             'is_superuser': False,
                             'is_merchant': False,
                             'organization': None,
                             'is_active': True,
                             'delete_request': None,
                             'created_by': {'id': self.merchant['id'],
                                            'email': self.merchant['email']}}

    @pytest.mark.skip
    def test_merchant_detail_created_worker(self):
        pass

    @pytest.mark.skip
    def test_merchant_update_created_worker(self):
        pass

    @pytest.mark.skip
    def test_merchant_delete_created_worker(self):
        pass

    @pytest.mark.skip
    def test_merchant_negative_create_superuser(self):
        pass

    @pytest.mark.skip
    def test_merchant_negative_create_admin(self):
        pass

    @pytest.mark.skip
    def test_merchant_negative_create_merchant(self):
        pass

    @pytest.mark.skip
    def test_merchant_negative_update_worker_status_to_upper(self):
        pass

    @pytest.mark.skip
    def test_merchant_negative_update_anyone_except_own_worker(self):
        pass

    @pytest.mark.skip
    def test_merchant_negative_delete_anyone_except_own_worker(self):
        pass

