from django.db import models, connection
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.db.models.functions import Coalesce

import apps.receipts.models as models_
from apps.receipts.managers import ProductManager, ProductCategoryManager
from apps.user_panel.models import CustomUser


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)  # orderLines[].category
    objects = ProductCategoryManager()

    def __repr__(self):
        return '{0}-{1}'.format(self.pk, self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    @staticmethod
    def get(order: dict):
        """
        @param orderLine: single order from storebox API
        @return: ProductCategory object
        """
        return ProductCategory(name=order['category'])


class Product(models.Model):
    """
    Can be very wide range or fairly specific
    Examples: pasta, tomatoes, milk
    """
    category = models.ForeignKey(ProductCategory,
                                 on_delete=models.CASCADE,
                                 null=True)
    name = models.CharField(max_length=255, unique=True)  # orderLines[].name
    number = models.CharField(max_length=255) # orderLines[].number
    objects = ProductManager()

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


    @staticmethod
    def get(order: dict, category: ProductCategory):
        """
        @param orderLine: single order from storebox API
        @return: ProductCategory object
        """
        return Product(name=order['name'],
                       number=order['number'],
                       category=category)

    @staticmethod
    def find_connections(org_id: int):
        """
        Find strongly connected products that customers buy often together.
        Calculate percentage of receipt with such products among all merchant data.
        Warning: slow db query. Don't use it often, cache and reuse results
        """
        # get rid of uncommon receipts
        min_receipts = 3
        limit = 50
        min_products = 3

        query = """
            WITH receipts AS (
                select array_agg(distinct {articles_tb}.product_id) as product_arr,
                {orders_tb}.receipt_id
                FROM {orders_tb}
                INNER JOIN {stores_tb} ON {orders_tb}.store_id = {stores_tb}.id
                INNER JOIN {users_tb}
                    ON {stores_tb}.merchant_id = {users_tb}.id
                    AND {users_tb}.organization_id = {org_id}
                INNER JOIN {articles_tb} ON ({orders_tb}.article_id = {articles_tb}.id)
                GROUP BY receipt_id
            ), product_groups AS (
                select product_arr, count(receipt_id) AS recs FROM receipts
                GROUP BY product_arr HAVING count(receipt_id) > {min_receipts}
            )

            select g1.product_arr,
                ((MAX(g1.recs) + coalesce(SUM(g2.recs) FILTER (WHERE g1.product_arr <@ g2.product_arr), 0)) /
                (
                    SUM(g2.recs) FILTER (WHERE g1.product_arr @> g2.product_arr) + MAX(g1.recs) +
                    coalesce(SUM(g2.recs) FILTER (WHERE g1.product_arr <@ g2.product_arr), 0)
                )) *100.0 AS correlation
            from product_groups AS g1
            INNER JOIN product_groups AS g2 ON (
                g1.product_arr <> g2.product_arr AND
                (g1.product_arr @> g2.product_arr OR g1.product_arr <@ g2.product_arr)
            )
            GROUP BY g1.product_arr HAVING array_length(g1.product_arr, 1) >= {min_products}
            ORDER BY correlation DESC LIMIT {limit};
        """.format(min_receipts=min_receipts, org_id=org_id,
                   limit=limit, min_products=min_products,
                   users_tb=CustomUser.objects.model._meta.db_table,
                   orders_tb=models_.OrderLine.objects.model._meta.db_table,
                   articles_tb=models_.Article.objects.model._meta.db_table,
                   receipts_tb=models_.Receipt.objects.model._meta.db_table,
                   stores_tb=models_.Store.objects.model._meta.db_table)

        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    @staticmethod
    def recommendations(product_ids: list, org_id: int):
        values = ','.join(['%s']*len(product_ids))
        query = """
            WITH receipt_with_products AS (
                SELECT q1.receipt_id, prods_ids, total, price FROM
                (
                    select receipt_id,
                    array_agg(distinct {articles_tb}.product_id) as prods_ids,
                    count(*) over () AS total
                FROM {orders_tb} INNER JOIN {stores_tb}
                    ON {stores_tb}.id = {orders_tb}.store_id
                INNER JOIN {users_tb}
                    ON {stores_tb}.merchant_id = {users_tb}.id
                    AND {users_tb}.organization_id = {org_id}
                INNER JOIN {receipts_tb}
                    ON {orders_tb}.receipt_id = {receipts_tb}.id
                INNER JOIN {articles_tb}
                    ON {orders_tb}.article_id = {articles_tb}.id
                GROUP BY receipt_id having ARRAY[{values}] <@ array_agg(product_id)) q1
                INNER JOIN {paymnets_tb} ON {paymnets_tb}.receipt_id = q1.receipt_id
            ),
            unwinded_products AS (
                SELECT unnest(prods_ids) AS product_id, total, price FROM
                receipt_with_products
            ),
            pop_articles as (
                select a.name as recs, count(*) as cnt, a.product_id
                from {orders_tb} as o INNER JOIN {articles_tb} as a ON o.article_id=a.id
                WHERE product_id NOT IN ({values})
                AND EXISTS (
                    SELECT 1
                    FROM unwinded_products as u_p
                    WHERE u_p.product_id=a.product_id
                )
                group by a.name, a.product_id
            ),
            rec_article AS (
                select product_id, recs
                FROM pop_articles as q1
                where cnt >= (
                    SELECT MAX(cnt)
                    from pop_articles
                    WHERE product_id=q1.product_id
                )
            )       

            SELECT id, name, number, percent, avg_order_value, recs FROM
            (SELECT product_id, count(*)*100.0 / total as percent,
                   avg(price) as avg_order_value FROM
            unwinded_products GROUP BY product_id, total
            HAVING product_id NOT IN ({values})) q1
            INNER JOIN {products_tb} ON {products_tb}.id = q1.product_id
            INNER JOIN rec_article ON rec_article.product_id = q1.product_id
            ORDER BY percent DESC;
        """.format(values=values, org_id=org_id,
                   users_tb=CustomUser.objects.model._meta.db_table,
                   orders_tb=models_.OrderLine.objects.model._meta.db_table,
                   articles_tb=models_.Article.objects.model._meta.db_table,
                   receipts_tb=models_.Receipt.objects.model._meta.db_table,
                   stores_tb=models_.Store.objects.model._meta.db_table,
                   products_tb=models_.Product.objects.model._meta.db_table,
                   paymnets_tb=models_.Payment.objects.model._meta.db_table)
        return Product.objects.raw(query, product_ids*3)

    @staticmethod
    def list_items(user):
        # use OrderLine model to avoid spanning multi-valued relationships
        # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
        return models_.OrderLine.objects \
            .filter(store__merchant__organization_id=user.organization_id) \
            .values('article__product') \
            .annotate(sold_items=Coalesce(Sum('count'), 0))

    @staticmethod
    def item_values(qs: QuerySet):
        return qs.values('article__product_id',
                         'article__product__name',
                         'article__product__number',
                         'article__product__category',
                         'sold_items')
