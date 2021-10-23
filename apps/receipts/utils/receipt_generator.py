from faker import Faker
import django
django.setup()

import string
import random

from backend.utils import randomString
from apps.members.models import Member
DIGITS_AND_ASCII = string.ascii_lowercase + string.digits
CURRENCY = "EUR"
VAT_PERCENT = 25

class ReceiptGenerator:
    """
    Provide tools to generate fake receipts in ARTS POSLog  format
    Receipt data example:
    https://developer.storebox.com/pos-api.html#operation/createReceipt
    https://developer.storebox.com/receipt-data-api.html#operation/getReceipt
    """
    def __init__(self, stores_count: int,
                 categories_count: int,
                 products_count: int,
                 articles_count: int,
                 members: list):

        self.fake = Faker()
        self.tz = self.fake.pytimezone()
        self.all_users = [self.getUserId(m) for m in members]
        self.all_stores = [self.getStore() for i in range(stores_count)]

        self.all_categories = [self.getCategory() for i in range(categories_count)]
        self.all_products = [self.getProduct(
            random.choice(self.all_categories)) for i in range(products_count)]
        self.all_articles = [self.getArticle(
            random.choice(self.all_products)) for i in range(articles_count)]


    def getUserId(self, member):
        return [{
            "type": "pan",
            "value": member.external_id
            }
        ]

    def date(self):
        return self.fake.date_time_between(start_date='-1y',
                                           tzinfo=self.tz).\
                                           strftime("%Y-%m-%dT%H:%M:%S%z")

    def barcode(self):
        val = self.fake.ean(length=13)
        return {
            "value": val,
            "displayValue": val,
            "type": "interleaved2of5"
        }

    def getStore(self):
        return {
            "storeName": self.fake.company(),
            "storeId": str(random.randint(0, 10000)),
            "storeRegNumber": randomString(8, string.digits),
            "storeAddressLine1": self.fake.address(),
            "storeZipCode": self.fake.postcode(),
            "storeCity": self.fake.city(),
            "storeCountry": self.fake.country(),
            "storePhone": self.fake.phone_number()
        }

    def getArticle(self, product):
        return {
            "gtin": randomString(13, string.digits),
            "name":  self.fake.bothify(text='Article-????-########'),
            "product": product
        }

    def getProduct(self, category):
        return {
            "name": self.fake.bothify(text='Product-????-########'),
            "number": randomString(5, string.digits),
            "category": category
        }

    def getCategory(self):
        return {
            "name": self.fake.bothify(text='Category-????-########')
        }

    def payment(self, price):
        return {
            "paymentType": "MASTERCARD",
            "priceValue": price,
            "priceCurrency": CURRENCY,
            "truncatedCardNumber": randomString(16, string.digits),
            "cardName": randomString(10, string.digits),
        }

    def orderLine(self, article):
        price = random.uniform(15, 100)
        count = random.randint(1, 7)
        vat = price * VAT_PERCENT/100
        totalVat = vat * count
        totalPrice = price * count

        return {
            "category": article['product']['category']['name'],
            "number": article['product']['number'],
            "name": article['product']['name'],
            "text": article['name'],
            "count": count,
            "gtin": article['gtin'],
            "itemPrice": {
                "value": price,
                "currency": CURRENCY,
                "vat": vat,
                "vatPercentage": VAT_PERCENT
            },
            "totalPrice": {
                "value": totalPrice,
                "currency": CURRENCY,
                "vat": totalVat,
                "vatPercentage": VAT_PERCENT
            },
            "type": "sale"
        }

    def getOrderList(self, count):
        orders = []
        for i in range(count):
            article = random.choice(self.all_articles)
            orders.append(self.orderLine(article))
        return orders

    def getReceipt(self):
        order_lines = self.getOrderList(random.randint(1,5))
        total_price = sum([o['totalPrice']['value'] for o in order_lines])

        return {
            "receiptId": randomString(32, DIGITS_AND_ASCII),
            "userId": random.choice(self.all_users),
            "merchantId": "storebox",
            "store": random.choice(self.all_stores),
            "orderDate": self.date(),
            "orderNumber": str(random.randint(0, 10000)),
            "salesEmployeeName": self.fake.name(),
            "headerText": [
                "Thank you for shopping with us"
            ],
            "footerText": [
                "You could have saved 10 kr. if you were a loyalty member",
                "Signup here https://storebox.com"
            ],
            "terminalId": randomString(15, string.digits),
            "sequenceNumber": str(random.randint(0, 10000)),
            "barcode": self.barcode(),
            "orderLines": order_lines,
            "totalOrderPrice": {
                "value": total_price,
                "currency": CURRENCY,
                "vatRates": [
                {
                    "rate": VAT_PERCENT,
                    "value": sum([o['totalPrice']['vat'] for o in order_lines]),
                    "currency": CURRENCY
                }
                ]
            },
            "payments": [
                self.payment(total_price)
            ]
        }


if __name__ == "__main__":
    members = Member.objects.all()
    generator = ReceiptGenerator(1,1,1,1,members)
    import json
    print(json.dumps(generator.getReceipt(), indent=4, sort_keys=True))
