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
