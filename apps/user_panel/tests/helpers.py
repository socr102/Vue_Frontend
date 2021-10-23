import json
from rest_framework.test import APIClient

from backend.settings import SUPERUSER_DATA
from faker import Faker

fake = Faker()
crescofy_accounts = ['admin@crescofy.com', 'christopher@crescofy.com']


def generate_user(admin: bool = False):
    return {
        'email': fake.email(),
        'password': fake.password(),
        'first_name': fake.name().split(' ')[0],
        'last_name': fake.name().split(' ')[1],
        'social_security': int(''.join(filter(str.isdigit, fake.ssn()))),
        'phone': int(''.join(filter(str.isdigit, fake.phone_number()))),
        'allow_contact': True,
        'is_staff': True if admin else False,
        'is_active': True,
        'is_merchant': False if admin else True,
        'contact_way': 'EM'
    }


def superuser_create_user(is_staff: bool):
    superuser_client = APIClient()
    superuser = superuser_client.post('/api/v1/token/', data=SUPERUSER_DATA).data
    superuser_client.credentials(HTTP_AUTHORIZATION='Bearer ' + superuser['access'])

    admin = generate_user(True if is_staff else False)
    admin['id'] = superuser_client.post('/api/v1/account/',
                                        content_type='application/json',
                                        data=json.dumps({'email': admin['email'],
                                                         'password': admin['password'],
                                                         'is_staff': True if is_staff else False,
                                                         'is_merchant': False if is_staff else True})).data['id']
    return admin


def create_merchant_by_admin(client: APIClient):
    merchant = generate_user()
    response = client.post('/api/v1/account/', content_type='application/json',
                           data=json.dumps({'email': merchant['email'],
                                            'password': merchant['password'],
                                            'is_merchant': True})).json()
    merchant['user_id'] = response['id']
    return merchant


def create_worker_by_merchant(client: APIClient):
    worker = generate_user()
    response = client.post('/api/v1/account/', content_type='application/json',
                           data=json.dumps({'email': worker['email'],
                                            'password': worker['password'],
                                            'is_worker': True})).json()
    worker['user_id'] = response['id']
    return worker
