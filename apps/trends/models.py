from datetime import date, datetime

from apps.receipts.models import Article, Product, OrderLine, Receipt, Store
from apps.user_panel.models import CustomUser

class Trend:

    orders_table = OrderLine.objects.model._meta.db_table
    receipts_table = Receipt.objects.model._meta.db_table
    stores_table = Store.objects.model._meta.db_table
    products_table = Product.objects.model._meta.db_table
    articles_table = Article.objects.model._meta.db_table

    @staticmethod
    def get_query_params(start: datetime, end: datetime):
        middle = start + (end - start)/2

        return [
            start, middle,
            middle, end,
            start, end
        ]

    @staticmethod
    def trending_articles(start: datetime, end: datetime, direction: str, org_id: int):
        """
        List articles with up/down saling trends.
        Include trend timeline
        """
        params = Trend.get_query_params(start, end)
        order = 'DESC' if direction == 'up' else 'ASC'
        limit = 5

        query = """
            WITH article_sales AS (
                SELECT {orders_tb}.article_id,
                    coalesce(sum({orders_tb}.count) FILTER (WHERE
                        {receipts_tb}.order_date >= %s AND {receipts_tb}.order_date < %s), 0) AS sales_0,
                    coalesce(sum({orders_tb}.count) FILTER (WHERE
                        {receipts_tb}.order_date >= %s AND {receipts_tb}.order_date < %s), 0) AS sales_1
                FROM {orders_tb}
                INNER JOIN {stores_tb} ON {orders_tb}.store_id = {stores_tb}.id
                INNER JOIN {users_tb}
                    ON {stores_tb}.merchant_id = {users_tb}.id
                    AND {users_tb}.organization_id = {org_id}
                INNER JOIN {receipts_tb}
                ON
                    {orders_tb}.receipt_id = {receipts_tb}.id
                    AND {receipts_tb}.order_date >= %s AND {receipts_tb}.order_date < %s
                GROUP BY 1)

            SELECT {articles_tb}.name, {articles_tb}.id, {articles_tb}.product_id,
                sales_1, sales_0,
                (sales_1 - sales_0) * 100 / COALESCE(NULLIF(sales_0, 0), 1) AS diff
            FROM article_sales INNER JOIN {articles_tb}
            ON article_sales.article_id = {articles_tb}.id
            ORDER BY 6 {order} LIMIT {limit};
        """.format(order=order, limit=limit, org_id=org_id,
                   users_tb=CustomUser.objects.model._meta.db_table,
                   orders_tb=Trend.orders_table,
                   articles_tb=Trend.articles_table,
                   receipts_tb=Trend.receipts_table,
                   stores_tb=Trend.stores_table)
        return Article.objects.raw(query, params)


    @staticmethod
    def trending_products(start: date, end: date,
                          direction: str, org_id: int):
        """
        List products with up/down saling trends.
        Include trend timeline
        """
        params = Trend.get_query_params(start, end)
        order = 'DESC' if direction == 'up' else 'ASC'
        limit = 5

        query = """
            WITH product_sales AS (
                SELECT {articles_tb}.product_id,
                    coalesce(sum({orders_tb}.count) FILTER (WHERE
                        {receipts_tb}.order_date >= %s AND {receipts_tb}.order_date < %s), 0) AS sales_0,
                    coalesce(sum({orders_tb}.count) FILTER (WHERE
                        {receipts_tb}.order_date >= %s AND {receipts_tb}.order_date < %s), 0) AS sales_1
                FROM {orders_tb}
                INNER JOIN {stores_tb} ON {orders_tb}.store_id = {stores_tb}.id
                INNER JOIN {users_tb}
                    ON {stores_tb}.merchant_id = {users_tb}.id
                    AND {users_tb}.organization_id = {org_id}
                INNER JOIN {receipts_tb}
                ON
                    {orders_tb}.receipt_id = {receipts_tb}.id
                    AND {receipts_tb}.order_date >= %s AND {receipts_tb}.order_date < %s
                INNER JOIN {articles_tb} ON
                    {orders_tb}.article_id = {articles_tb}.id
                GROUP BY 1)

            SELECT {products_tb}.name, {products_tb}.id, sales_1, sales_0,
                (sales_1 - sales_0) * 100 / COALESCE(NULLIF(sales_0, 0), 1) AS diff
            FROM product_sales INNER JOIN {products_tb}
            ON product_sales.product_id = {products_tb}.id
            ORDER BY 5 {order} LIMIT {limit};
        """.format(order=order, limit=limit, org_id=org_id,
                   users_tb=CustomUser.objects.model._meta.db_table,
                   orders_tb=Trend.orders_table,
                   articles_tb=Trend.articles_table,
                   receipts_tb=Trend.receipts_table,
                   stores_tb=Trend.stores_table,
                   products_tb=Trend.products_table)
        return Product.objects.raw(query, params)
