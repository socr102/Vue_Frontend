from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .utils import DIRECTIONS

trend_schema = extend_schema(
    parameters=[
        OpenApiParameter("direction",
                         OpenApiTypes.STR,
                         OpenApiParameter.PATH,
                         enum=DIRECTIONS,
                         description="Specify direction of a trend"
                        )
    ]
)
