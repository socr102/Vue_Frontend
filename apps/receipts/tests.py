import random
from datetime import datetime

import pytest
from django.test import TestCase
from rest_framework.test import APIClient

from backend.settings import SUPERUSER_DATA
from .models import Article, Product, ProductCategory, Receipt, Store, OrderLine
from apps.user_panel.models import CustomUser


data_to_populate = {'category': 'diary',
                    'product': {
                        'milk': ['Apple', 'Google', 'Microsoft', 'Amazon'],
                        'cheese': ['Amazon', 'Facebook', 'Coca-Cola', 'Disney'],
                        'pasta': ['Disney', 'Samsung', 'Louis Vuitton', 'McDonalds']
                    }
                    }


def populate_articles():
    articles = list()
    category = ProductCategory.objects.create(name=data_to_populate['category'])
    for product, populated_articles in data_to_populate['product'].items():
        product = Product.objects.create(category=category, name=product)
        for article in populated_articles:
            articles.append(Article.objects.create(name=article, product=product))
    return articles


def populate_orders(articles: list):
    receipts = [Receipt.objects.create(sales_employee_name='Ivan', order_date=datetime.now()) for _ in range(10)]
    store = Store.objects.create(name='store')
    for _ in range(100):
        OrderLine.objects.create(article=random.choice(articles),
                                 receipt=random.choice(receipts),
                                 store=store,
                                 count=random.randint(1, 5),
                                 currency='USD',
                                 item_vat=0.1,
                                 item_price=float(random.uniform(1.5, 1.9))
                                 )


@pytest.mark.django_db
class TestApiView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        CustomUser.objects.create_user(email=SUPERUSER_DATA['email'],
                                       password=SUPERUSER_DATA['password'],
                                       is_superuser=True)
        self.SUPERUSER = self.client.post('/api/v1/token/', data=SUPERUSER_DATA).data['access']

    def test_get_superuser_token(self):
        response = self.client.post('/api/v1/token/', data=SUPERUSER_DATA)
        assert response.status_code == 200
        result = response.json()
        pytest.bearer = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + result['access'])

    def test_related_article(self):
        article_ids = populate_articles()
        populate_orders(article_ids)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.SUPERUSER)
        response = self.client.get('/api/v1/article/related/', data={'target_articles': [random.choice(article_ids).id,
                                                                                  random.choice(article_ids).id,
                                                                                  ]})
        assert response
