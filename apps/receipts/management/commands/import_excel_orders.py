from __future__ import annotations

from typing import Union
from collections import defaultdict
from collections.abc import Iterable
import pytz
import string
import random

from django.core.management.base import BaseCommand, CommandError

import openpyxl
from openpyxl.cell.cell import Cell
from faker import Faker

from apps.members.models import Member
import apps.receipts.models as rec_models
from backend.utils import positive_int, randomString
import apps.user_panel.models as user_models


class Command(BaseCommand):
    help = 'Import receipts and members to Database from external excel file'

    _CURRENCY         = 'SEK'
    _STORE_NAME       = 'Merchant'
    _RECEIPT_ID       = 'Order ID'
    _RECEIPT_DATE     = 'Date'
    _MEMBER_NAME      = 'Customer Name'
    _MEMBER_EMAIL     = 'Email'
    _MEMBER_EXT_ID    = 'Customer ID'
    _ARTICLE_EXT_ID   = 'Product ID'
    _ARTICLE_NAME     = 'Product Name'
    _PRODUCT_NAME     = 'L2'
    _CATEGORY_NAME    = 'L1'
    _ORDER_PRICE      = 'Ordered TO (SEK)'
    _ORDER_ITEM_COUNT = 'Qty Ordered'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._stores = dict()
        self._members = dict()
        self._articles = dict()
        self._products = dict()
        self._categories = dict()
        self._orderlines = list()
        self._receipts = dict()
        self._payments = dict()
        self._payment_price = defaultdict(int)
        self.fields = None
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('--filepath', type=str, required=True, help='')
        parser.add_argument('--merchantId', type=positive_int, required=True, help='')

    def set_ws_fields(self, ws: Iterable[list[Cell]]):
        """Retruns mapper between field name and position within a row."""
        _, _ = next(ws), next(ws)
        row = next(ws)
        self.fields = {field.value: idx for idx, field in enumerate(row)}

    def get_merchant(self, options) -> user_models.CustomUser:
        merchant = user_models.CustomUser.objects.filter(id=options['merchantId'],
                                                         is_active=True).first()

        if not merchant:
            raise CommandError("There is no merchants in Database with provided id")

        return merchant

    def get_value(self, row: list[Cell], field: str) -> Union[str, None]:
        """Get field value from a xlsx row."""
        idx = self.fields.get(field)
        if idx is None:
            self.stdout.write(self.style.WARNING(f"Can't find {field} in a {row}."))
            return None

        return row[idx].value

    def add_member(self, row: list[Cell], merchant: user_models.CustomUser):
        external_id = self.get_value(row, self._MEMBER_EXT_ID)
        if self._members.get(external_id):
            return

        email = self.get_value(row, self._MEMBER_EMAIL)
        if not email:
            email = self.fake.email()
        sex = Member.SEX_CHOICES[random.randint(0, 1)][0]
        birth = self.fake.date_between(start_date='-70y', end_date='-20y')
        member = Member(external_id=external_id,
                        organization_id=merchant.organization_id,
                        name=self.get_value(row, self._MEMBER_NAME),
                        sex=sex,
                        birth_date=birth,
                        email=email)
        self._members[external_id] = member

    def add_receipt(self, row: list[Cell]):
        external_id = self.get_value(row, self._RECEIPT_ID)
        if self._receipts.get(external_id):
            return

        order_date = self.get_value(row, self._RECEIPT_DATE) \
                         .replace(tzinfo=pytz.UTC)
        receipt = rec_models.Receipt(order_date=order_date,
                                     sales_employee_name=self.fake.name())
        self._receipts[external_id] = receipt

    def add_orderline(self, row: list[Cell]):
        receipt_id = self.get_value(row, self._RECEIPT_ID)
        member_id = self.get_value(row, self._MEMBER_EXT_ID)
        store_id = self.get_value(row, self._STORE_NAME)
        article_id = self.get_value(row, self._ARTICLE_EXT_ID)

        item_count = self.get_value(row, self._ORDER_ITEM_COUNT)
        price = self.get_value(row, self._ORDER_PRICE)
        if not item_count:
            return

        item_price = float(price) / item_count

        orderline = rec_models.OrderLine(receipt=self._receipts[receipt_id],
                                         member=self._members[member_id],
                                         store=self._stores[store_id],
                                         article=self._articles[article_id],
                                         item_vat=0,
                                         currency=self._CURRENCY,
                                         item_price=item_price,
                                         count=item_count)
        self._orderlines.append(orderline)

    def add_store(self, row: list[Cell], merchant: user_models.CustomUser):
        external_id = self.get_value(row, self._STORE_NAME)
        if self._stores.get(external_id):
            return

        store = rec_models.Store(name=external_id,
                                 external_id=external_id,
                                 merchant=merchant,
                                 reg_number=randomString(8, string.digits),
                                 address=self.fake.address(),
                                 zipcode=self.fake.postcode(),
                                 city=self.fake.city(),
                                 country=external_id,
                                 phone=self.fake.phone_number())
        self._stores[external_id] = store

    def add_payment(self, receipt: rec_models.Receipt, receipt_id: str):
        if self._payments.get(receipt_id):
            return

        price = self._payment_price[receipt_id]
        payment = rec_models.Payment(payment_type='INVOICE',
                                     price=price,
                                     receipt=receipt,
                                     truncated_card_number='XXXXXXXXXXXX1234',
                                     currency=self._CURRENCY)
        self._payments[receipt_id] = payment

    def add_article(self, row: list[Cell]):
        external_id = self.get_value(row, self._ARTICLE_EXT_ID)
        if self._articles.get(external_id):
            return

        product_id = self.get_value(row, self._PRODUCT_NAME)
        article = rec_models.Article(name=self.get_value(row, self._ARTICLE_NAME),
                                     number=external_id,
                                     gtin=randomString(13, string.digits),
                                     product=self._products[product_id])
        self._articles[external_id] = article

    def add_product(self, row: list[Cell]):
        external_id = self.get_value(row, self._PRODUCT_NAME)
        if self._products.get(external_id):
            return

        category_id = self.get_value(row, self._CATEGORY_NAME)
        product = rec_models.Product(name=external_id,
                                     number="0",
                                     category=self._categories[category_id])
        self._products[external_id] = product

    def add_product_category(self, row: list[Cell]):
        external_id = self.get_value(row, self._CATEGORY_NAME)
        if self._categories.get(external_id):
            return

        category = rec_models.ProductCategory(name=external_id)
        self._categories[external_id] = category

    def calculate_payment_price(self, row: list[Cell]):
        receipt_id = self.get_value(row, self._RECEIPT_ID)
        orderline_price = float(self.get_value(row, self._ORDER_ITEM_COUNT))
        self._payment_price[receipt_id] += orderline_price

    def handle(self, *args, **options) -> None:
        merchant = self.get_merchant(options)

        wb = openpyxl.load_workbook(filename=options['filepath'])
        ws = iter(wb.active)
        self.set_ws_fields(ws)

        for row in ws:
            self.add_member(row, merchant)
            self.add_receipt(row)
            self.add_product_category(row)
            self.add_product(row)
            self.add_article(row)
            self.add_store(row, merchant)
            self.add_orderline(row)
            self.calculate_payment_price(row)

        for id_, item in self._receipts.items():
            self.add_payment(item, id_)

        members = {m.external_id: m
                  for m in Member.objects.bulk_create(self._members.values())}

        for order in self._orderlines:
            order.member = members[order.member.external_id]

        rec_models.Receipt.upsert_data(self._orderlines,
                            self._receipts.values(),
                            self._articles.values(),
                            self._stores.values(),
                            self._categories.values(),
                            self._products.values(),
                            self._payments.values())


