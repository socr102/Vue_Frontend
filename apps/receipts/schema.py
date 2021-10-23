from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes

from backend import utils

list_campaigns_schema = extend_schema(
    parameters=[
        OpenApiParameter("order",
                         OpenApiTypes.STR,
                         OpenApiParameter.QUERY,
                         enum=["end_date", "-end_date"],
                         description=utils.ORDER_FILTER_DESC),
        OpenApiParameter("limit",
                         OpenApiTypes.INT,
                         OpenApiParameter.QUERY,
                         description="Number of results to return per page.")
    ],
    methods=['GET']
)


list_article_recs_schema = extend_schema(
    parameters=[
        OpenApiParameter("article",
                         OpenApiTypes.INT,
                         OpenApiParameter.QUERY,
                         description=("Article id. Allow to pass list of values"
                                      " using the same field. Example: ?article=1&article=2")),
    ],
    methods=['GET']
)

list_product_recs_schema = extend_schema(
    parameters=[
        OpenApiParameter("product",
                         OpenApiTypes.INT,
                         OpenApiParameter.QUERY,
                         description=("Product id. Allow to pass list of values"
                                      " using the same field. Example: ?product=1&product=2")),
    ],
    methods=['GET']
)

