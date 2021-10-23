from django.db import models, connection

from apps.offers.models import Offer
from apps.audience.models import Audience
import apps.receipts.models as rec_models

class Campaign(models.Model):
    name = models.CharField(max_length=256)
    organization = models.ForeignKey('organizations.Organization',
                                     on_delete=models.SET_NULL,
                                     null=True)
    offer = models.ForeignKey('offers.Offer',
                              on_delete=models.SET_NULL,
                              null=True)
    audience = models.ForeignKey('audience.Audience',
                              on_delete=models.SET_NULL,
                              null=True)

    @property
    def is_archive(self):
        return self.offer.is_archive

    @property
    def is_active(self):
        return self.offer.is_active

    # pre-computed data asociated with a campaign:
    # statistics, status etc
    REVENUE               = 'revenue'
    TOTAL_AUDIENCE        = 'campaign_members'
    PARTICIPATED_AUDIENCE = 'members_participated'
    metadata = models.JSONField(default=dict)

    upd_metadata = f"""
        json_build_object(
            '{TOTAL_AUDIENCE}', campaigns_meta.c_members_len,
            '{REVENUE}', campaigns_meta.revenue,
            '{PARTICIPATED_AUDIENCE}', campaigns_meta.members_len
        )
    """

    @staticmethod
    def member_campaigns(filter_by: str) -> str:
        return """
            member_campaigns AS (
                SELECT
                    start_date, end_date, article_id, {{campaigns_tb}}.id AS campaign_id
                FROM {{campaigns_tb}} INNER JOIN {{offer_tb}} ON
                {{campaigns_tb}}.offer_id = {{offer_tb}}.id AND
                {{campaigns_tb}}.{filter_by} = %s
                INNER JOIN {{off_articles_tb}} ON
                {{off_articles_tb}}.offer_id = {{campaigns_tb}}.offer_id
                INNER JOIN {{aud_mem_tb}} ON
                {{campaigns_tb}}.audience_id = {{aud_mem_tb}}.audience_id
                AND {{aud_mem_tb}}.member_id = %s
            )
        """.format(filter_by=filter_by)

    @staticmethod
    def deduplicate_campaigns():
        return """
            deduplicated_campaigns AS (
                SELECT campaign_id, start_date, end_date,
                array_agg(DISTINCT article_id) AS с_articles
                FROM member_campaigns GROUP BY campaign_id, start_date, end_date
            )
        """

    @staticmethod
    def list_member_campaigns(member_id: int, org_id: int,
                              order: str, limit: int):
        query = _SQL_MEMBER_CAMPAIGNS.format(campaigns_tb=Campaign.objects.model._meta.db_table,
                   aud_mem_tb=Audience.members.through.objects.model._meta.db_table,
                   off_articles_tb=Offer.articles.through.objects.model._meta.db_table,
                   offer_tb=Offer.objects.model._meta.db_table,
                   audience_tb=Audience.objects.model._meta.db_table,
                   orders_tb=rec_models.OrderLine.objects.model._meta.db_table,
                   receipts_tb=rec_models.Receipt.objects.model._meta.db_table,
                   order=order)

        campaigns = list(Campaign.objects.raw(query, [org_id, member_id,
                                                      member_id, limit]))
        for c in campaigns:
            # add offer and audience relations manually to prevent DB hit
            c.offer = Offer(id=c.offer_id, name=c.offer_name,
                            end_date=c.offer_end_date,
                            start_date=c.offer_start_date)
            c.audience = Audience(id=c.audience_id, name=c.audience_name)

        return campaigns

    @staticmethod
    def list_member_campaign_activities(member_id, campaign_id, limit):
        query = _SQL_MEMBER_ACTIVITIES.format(campaigns_tb=Campaign.objects.model._meta.db_table,
                   aud_mem_tb=Audience.members.through.objects.model._meta.db_table,
                   off_articles_tb=Offer.articles.through.objects.model._meta.db_table,
                   offer_tb=Offer.objects.model._meta.db_table,
                   audience_tb=Audience.objects.model._meta.db_table,
                   stores_tb=rec_models.Store.objects.model._meta.db_table,
                   articles_tb=rec_models.Article.objects.model._meta.db_table,
                   orders_tb=rec_models.OrderLine.objects.model._meta.db_table,
                   receipts_tb=rec_models.Receipt.objects.model._meta.db_table)

        orders = list(rec_models.OrderLine.objects.raw(query, [campaign_id, member_id,
                                                                 member_id, limit]))
        for o in orders:
            # add article and store relations manually to prevent DB hit
            o.article = rec_models.Article(id=o.article_id, name=o.article_name)
            o.store = rec_models.Store(id=o.store_id, name=o.store_name)

        return orders

    @staticmethod
    def collect_metadata():
        """
            Collect campaigns statistics and metadata.
            Update campaigns metadata as a JSON.
            Heavy query, avoid to use it in a user request
        """
        query = """
            WITH campaigns_info AS (
                SELECT
                    start_date, end_date, {campaigns_tb}.offer_id,
                    member_id, article_id, {campaigns_tb}.id as campaign_id
                FROM {campaigns_tb} INNER JOIN {offer_tb} ON
                {campaigns_tb}.offer_id = {offer_tb}.id
                INNER JOIN {off_articles_tb} ON
                {off_articles_tb}.offer_id = {campaigns_tb}.offer_id
                INNER JOIN {aud_mem_tb} ON
                {campaigns_tb}.audience_id = {aud_mem_tb}.audience_id
            ),

            deduplicated_campaigns_info AS (
                SELECT campaign_id, start_date, end_date,
                array_agg(distinct member_id) AS с_members,
                array_agg(distinct article_id) AS с_articles
                FROM campaigns_info group by campaign_id, start_date, end_date
            ),

            filtered_orders AS (
                SELECT {payments_tb}.price, article_id, array_length(с_members, 1) AS c_members_len,
                    member_id, campaign_id, с_articles, {orders_tb}.receipt_id
                FROM {orders_tb} INNER JOIN
                {receipts_tb} ON {receipts_tb}.id = {orders_tb}.receipt_id
                INNER JOIN
                {payments_tb} ON {payments_tb}.receipt_id = {orders_tb}.receipt_id

                INNER JOIN deduplicated_campaigns_info ON
                {receipts_tb}.order_date > deduplicated_campaigns_info.start_date AND
                {receipts_tb}.order_date < deduplicated_campaigns_info.end_date AND
                {orders_tb}.member_id = ANY(deduplicated_campaigns_info.с_members)
            ),

            grouped_orders AS (
                SELECT array_agg(distinct article_id) AS r_articles,
                c_members_len, с_articles, campaign_id, price, member_id FROM filtered_orders
                group by receipt_id, c_members_len, с_articles, campaign_id, price, member_id
            ),

            campaigns_meta AS (
                SELECT campaign_id, sum(price) AS revenue, c_members_len,
                    count(distinct member_id) AS members_len
                FROM grouped_orders
                WHERE с_articles <@ r_articles group by campaign_id, c_members_len
            )

            UPDATE {campaigns_tb} SET
            metadata={upd_metadata} from campaigns_meta
            WHERE {campaigns_tb}.id = campaigns_meta.campaign_id RETURNING *;
        """.format(upd_metadata=Campaign.upd_metadata,
                   campaigns_tb=Campaign.objects.model._meta.db_table,
                   offer_tb=Offer.objects.model._meta.db_table,
                   aud_mem_tb=Audience.members.through.objects.model._meta.db_table,
                   off_articles_tb=Offer.articles.through.objects.model._meta.db_table,
                   orders_tb=rec_models.OrderLine.objects.model._meta.db_table,
                   payments_tb=rec_models.Payment.objects.model._meta.db_table,
                   receipts_tb=rec_models.Receipt.objects.model._meta.db_table)

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows


_SQL_MEMBER_ACTIVITIES = "WITH {0}, {1},".format(Campaign.member_campaigns('id'),
                                                 Campaign.deduplicate_campaigns()) \
                        + """
                            member_receipts AS (
                                SELECT * FROM (
                                    SELECT receipt_id, array_agg(DISTINCT article_id) AS articles
                                    FROM {orders_tb} WHERE {orders_tb}.member_id = %s
                                    GROUP BY {orders_tb}.receipt_id) AS q
                                INNER JOIN {receipts_tb} ON {receipts_tb}.id = q.receipt_id
                            ),
                            member_campaign_receipts AS (
                                SELECT receipt_id, order_date FROM member_receipts
                                INNER JOIN deduplicated_campaigns ON
                                с_articles <@ articles AND start_date < order_date AND end_date > order_date
                                GROUP BY receipt_id, order_date
                            )

                            SELECT {orders_tb}.*,
                            {articles_tb}.name AS article_name,
                            {stores_tb}.name AS store_name
                            FROM {orders_tb}
                            INNER JOIN member_campaign_receipts ON
                            member_campaign_receipts.receipt_id = {orders_tb}.receipt_id
                            INNER JOIN {articles_tb} ON {orders_tb}.article_id = {articles_tb}.id
                            INNER JOIN {stores_tb} ON {orders_tb}.store_id = {stores_tb}.id
                            ORDER BY member_campaign_receipts.order_date DESC LIMIT %s;
                        """

_SQL_MEMBER_CAMPAIGNS = "WITH {0}, {1},".format(Campaign.member_campaigns('organization_id'),
                                                Campaign.deduplicate_campaigns()) \
                        + """
                            member_receipts AS (
                                SELECT * FROM (
                                    SELECT receipt_id, array_agg(DISTINCT article_id) AS articles
                                    FROM {orders_tb} WHERE {orders_tb}.member_id = %s
                                    GROUP BY {orders_tb}.receipt_id) AS q
                                INNER JOIN {receipts_tb} ON {receipts_tb}.id = q.receipt_id
                            ),
                            member_participated_campaign_ids AS (
                                SELECT campaign_id FROM member_receipts
                                INNER JOIN deduplicated_campaigns ON
                                с_articles <@ articles AND start_date < order_date AND end_date > order_date
                                GROUP BY campaign_id
                            )

                            SELECT campaigns.*,
                            {offer_tb}.name AS offer_name,
                            {offer_tb}.start_date AS offer_start_date,
                            {offer_tb}.end_date AS offer_end_date,
                            {audience_tb}.name AS audience_name

                            FROM (SELECT * FROM {campaigns_tb} WHERE id IN
                            (SELECT * FROM member_participated_campaign_ids)) AS campaigns
                            INNER JOIN {offer_tb} ON campaigns.offer_id = {offer_tb}.id
                            INNER JOIN {audience_tb} ON campaigns.audience_id = {audience_tb}.id
                            ORDER BY {offer_tb}.end_date {order} LIMIT %s;
                        """
