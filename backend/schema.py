from typing import Callable

from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_filters.rest_framework import FilterSet

from .utils import DjangoFilterOpenApi

auth_schema = extend_schema(
    responses=TokenObtainPairSerializer
)

def list_schema(filter_: FilterSet) -> Callable[..., Callable]:
    openapi = DjangoFilterOpenApi()
    parameters = []
    for base_field, filter_field in filter_.base_filters.items():
        parameters.extend(openapi.get_param(base_field, filter_field))

    return extend_schema(parameters=parameters, methods=['GET'])
