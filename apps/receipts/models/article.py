from __future__ import annotations

from django.db import models, connection
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.db.models.functions import Coalesce
import django.contrib.postgres.indexes as pg_indexes

import apps.receipts.models as models_
from apps.receipts.managers import ArticleManager
from apps.user_panel.models import CustomUser

class Article(models.Model):
    """
    Concrete(very specific) item in a store.
    Examples: Arla Organic Full fat 200ml, Barilla no.2 or Nike air xxxx
    Article is a subset of Product
    """
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE,
                                null=True)
    name = models.CharField(max_length=255)  # orderLines[].text
    number = models.CharField(max_length=255, null=True)
    gtin = models.CharField(max_length=13,
                            null=True,
                            unique=True)  # orderLines[].gtin
    objects = ArticleManager()

    class Meta:
       indexes = [pg_indexes.GistIndex(name="article_trgm_idx",
                                      fields=("name",),
                                      opclasses=("gist_trgm_ops",))]


    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.gtin)

    def __eq__(self, other):
        return self.gtin == other.gtin

    @staticmethod
    def bought_together(org_id: int, article_ids: list):
        print(article_ids)
        values = ','.join(['%s']*len(article_ids))
        query = """
            SELECT article_id, article_name, category, total_bt FROM (
                SELECT art_prod.article_id, art_prod.article_name, art_prod.category, cnts.total_bt,
                    ROW_NUMBER() OVER (PARTITION BY art_prod.category ORDER BY cnts.total_bt DESC) bt_rank
                FROM (
                    SELECT d.bought_with, SUM(d.times_bt) as total_bt
                    FROM (
                        SELECT c.original_id, c.bought_with, count(*) AS times_bt
                        FROM ( 
                            SELECT a.article_id as original_id, b.article_id AS bought_with
                            FROM {orders_tb} a
                            INNER JOIN {orders_tb} b
                            ON a.receipt_id=b.receipt_id AND a.article_id != b.article_id
                        ) c
                        WHERE c.original_id IN ({values})
                        AND c.bought_with NOT IN ({values})
                        GROUP BY c.original_id, c.bought_with
                        ) d
                    GROUP BY d.bought_with
                ) cnts
                INNER JOIN (
                    SELECT a.name AS article_name, a.id AS article_id, b.name as category
                    FROM {articles_tb} a
                    INNER JOIN {products_tb} b
                    ON a.product_id=b.id
                ) art_prod
                ON cnts.bought_with=art_prod.article_id
                ORDER BY cnts.total_bt DESC
            ) ft
            WHERE ft.bt_rank=1
            LIMIT 3;

        """.format(values=values, org_id=org_id,
                   orders_tb=models_.OrderLine.objects.model._meta.db_table,
                   articles_tb=models_.Article.objects.model._meta.db_table,
                   products_tb=models_.Product.objects.model._meta.db_table)

        with connection.cursor() as cursor:
            cursor.execute(query, article_ids*2)
            return cursor.fetchall()



    @staticmethod
    def recommendations(article_ids: list, org_id: int):
        values = ','.join(['%s']*len(article_ids))
        query = """
            WITH receipt_with_articles AS (
                SELECT q1.receipt_id, art_ids, total, price FROM
                (
                    select receipt_id,
                    array_agg(distinct article_id) as art_ids,
                    count(*) over () AS total
                FROM {orders_tb} INNER JOIN {stores_tb}
                    ON {stores_tb}.id = {orders_tb}.store_id
                INNER JOIN {users_tb}
                    ON {stores_tb}.merchant_id = {users_tb}.id
                    AND {users_tb}.organization_id = {org_id}
                INNER JOIN {receipts_tb}
                    ON {orders_tb}.receipt_id = {receipts_tb}.id
                GROUP BY receipt_id having ARRAY[{values}] <@ array_agg(article_id)) q1
                INNER JOIN {paymnets_tb} ON {paymnets_tb}.receipt_id = q1.receipt_id
            ),
            unwinded_articles AS (
                SELECT unnest(art_ids) AS article_id, total, price FROM
                receipt_with_articles
            )

            SELECT id, name, product_id, percent, avg_order_value FROM
            (SELECT article_id, count(*)*100.0 / total as percent,
                   avg(price) as avg_order_value FROM
            unwinded_articles GROUP BY article_id, total
            HAVING article_id NOT IN ({values})) q1
            INNER JOIN {articles_tb} ON {articles_tb}.id = q1.article_id
            ORDER BY percent DESC;
        """.format(values=values, org_id=org_id,
                   users_tb=CustomUser.objects.model._meta.db_table,
                   orders_tb=models_.OrderLine.objects.model._meta.db_table,
                   articles_tb=models_.Article.objects.model._meta.db_table,
                   receipts_tb=models_.Receipt.objects.model._meta.db_table,
                   stores_tb=models_.Store.objects.model._meta.db_table,
                   paymnets_tb=models_.Payment.objects.model._meta.db_table)
        return Article.objects.raw(query, article_ids*2)

    @staticmethod
    def find_connections(org_id: int, product_ids: list[int]):
        min_receipts, min_articles, limit = 3, 2, 50
        products_in = ','.join(['%s'] * len(product_ids))

        query = """
            WITH receipts AS (
                select array_agg(distinct {articles_tb}.id) as article_arr,
                {orders_tb}.receipt_id
                FROM {orders_tb}
                INNER JOIN {stores_tb} ON {orders_tb}.store_id = {stores_tb}.id
                INNER JOIN {users_tb}
                    ON {stores_tb}.merchant_id = {users_tb}.id
                    AND {users_tb}.organization_id = {org_id}
                INNER JOIN {articles_tb} ON (
                    {orders_tb}.article_id = {articles_tb}.id AND
                    {articles_tb}.product_id IN ({products_in})
                )
                GROUP BY receipt_id
            ), item_groups AS (
                select article_arr, count(receipt_id) AS recs FROM receipts
                GROUP BY article_arr HAVING count(receipt_id) > {min_receipts}
            ), connected_items AS (
                select g1.article_arr,
                    ((MAX(g1.recs) + coalesce(SUM(g2.recs) FILTER (WHERE g1.article_arr <@ g2.article_arr), 0)) /
                    (
                        SUM(g2.recs) FILTER (WHERE g1.article_arr @> g2.article_arr) + MAX(g1.recs) +
                        coalesce(SUM(g2.recs) FILTER (WHERE g1.article_arr <@ g2.article_arr), 0)
                    )) *100.0 AS correlation
                from item_groups AS g1
                INNER JOIN item_groups AS g2 ON (
                    g1.article_arr <> g2.article_arr AND
                    (g1.article_arr @> g2.article_arr OR g1.article_arr <@ g2.article_arr)
                )
                GROUP BY g1.article_arr HAVING array_length(g1.article_arr, 1) >= {min_articles}
            )

            SELECT json_agg(json_build_object(
                'id', g1.article_id, 'name', {articles_tb}.name, 'product', {products_tb}.name)
                ), correlation FROM (
                SELECT unnest(article_arr) AS article_id, article_arr, correlation
                FROM connected_items WHERE correlation IS NOT NULL
            ) AS g1
            INNER JOIN {articles_tb} ON article_id = {articles_tb}.id
            INNER JOIN {products_tb} ON {products_tb}.id = {articles_tb}.product_id
            GROUP BY article_arr, correlation ORDER BY correlation DESC LIMIT {limit};
        """.format(min_receipts=min_receipts,
                   org_id=org_id, products_in=products_in,
                   limit=limit, min_articles=min_articles,
                   users_tb=CustomUser.objects.model._meta.db_table,
                   orders_tb=models_.OrderLine.objects.model._meta.db_table,
                   articles_tb=models_.Article.objects.model._meta.db_table,
                   products_tb=models_.Product.objects.model._meta.db_table,
                   receipts_tb=models_.Receipt.objects.model._meta.db_table,
                   stores_tb=models_.Store.objects.model._meta.db_table)

        with connection.cursor() as cursor:
            cursor.execute(query, product_ids)
            return cursor.fetchall()

    @staticmethod
    def get(order: dict, product):
        """
        @param orderLine: single order from storebox API
        @return: Article object
        """
        return Article(gtin=order['gtin'],
                       name=order['text'],
                       product=product)

    @staticmethod
    def list_items(user):
        # use OrderLine model to avoid spanning multi-valued relationships
        # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
        return models_.OrderLine.objects \
            .filter(store__merchant__organization_id=user.organization_id) \
            .values('article') \
            .annotate(sold_items=Coalesce(Sum('count'), 0))

    @staticmethod
    def item_values(qs: QuerySet):
        return qs.values('article__name', 'sold_items', 'article_id',
                         'article__product', 'article__gtin')
