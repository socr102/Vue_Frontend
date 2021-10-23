from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.receipts.models import (Article, OrderLine, Product,
                             ProductCategory, Store, Payment)


class Receipt(models.Model):
    sales_employee_name = models.CharField(max_length=255) # salesEmployeeName
    order_date = models.DateTimeField()  # orderDate

    def __repr__(self):
        return '{0}-{1}'.format(self.pk, self.order_date)

    @staticmethod
    def bulk_import(receipts: list, merchant, members: list):
        """
        Parse JSON receipts and create appropriate models
        """
        category_set, product_set = set(), set()
        store_set, article_set = set(), set()
        order_set, receipt_set, payment_set = [], [], []

        for r in receipts:
            store = Store.get(r['store'], merchant)
            receipt = Receipt.get(r)
            receipt_set.append(receipt)
            store_set.add(store)

            filter_func = lambda m: m.external_id == r['userId'][0]['value'] \
                if r['userId'] else None
            member = next(filter(filter_func, members), None)

            for payment in r['payments']:
                payment_set.append(Payment.get(payment, receipt))

            for order in r['orderLines']:
                category = ProductCategory.get(order)
                product  = Product.get(order, category)
                article  = Article.get(order, product)

                category_set.add(category)
                article_set.add(article)
                product_set.add(product)
                order_set.append(OrderLine.get(order, article, store, receipt, member))

        Receipt.upsert_data(order_set,
                            receipt_set,
                            article_set,
                            store_set,
                            category_set,
                            product_set,
                            payment_set)
        return order_set

    @staticmethod
    def upsert_data(order_set, receipt_set, article_set, store_set,
                    category_set, product_set, payment_set):
        """
        Perform upsert operations on input models
        """
        categories = {c.name: c for c in ProductCategory.objects.\
            bulk_upsert(category_set)}
        stores = {hash(s): s for s in Store.objects.\
            bulk_upsert(store_set)}

        for p in product_set: p.category = categories[p.category.name]
        products = {p.name: p for p in Product.objects.\
            bulk_upsert(product_set)}

        for a in article_set: a.product = products[a.product.name]
        articles = {a.gtin: a for a in Article.objects.\
            bulk_upsert(article_set)}

        Receipt.objects.bulk_create(receipt_set)

        for p in payment_set:
            p.receipt_id = p.receipt.pk
        Payment.objects.bulk_create(payment_set)

        for o in order_set:
            o.article = articles[o.article.gtin]
            o.receipt_id = o.receipt.pk
            o.store = stores[hash(o.store)]
        OrderLine.objects.bulk_create(order_set)

    @staticmethod
    def get(receipt: dict):
        """
        @param receipt: detailed receipt from storebox API
        @return: Receipt object
        """
        return Receipt(sales_employee_name=receipt['salesEmployeeName'],
                       order_date=receipt['orderDate'])
