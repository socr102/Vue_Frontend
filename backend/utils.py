from __future__ import annotations

import random
import argparse

from django_filters.rest_framework import filters, Filter
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.contrib.django_filters import DjangoFilterExtension


def positive_int(x):
    """ argparse validator """
    x = int(x)
    if x < 1:
        raise argparse.ArgumentTypeError("Minimum value is 1")
    return x

def randomString(length, choices):
    return ''.join(random.choices(choices, k=length))


class DjangoFilterOpenApi:
    """Custom drf_spectacular extension for django_filter.
    Generate OpenApiParameter for each filter field
    """
    def __init__(self) -> None:
        self.extension = DjangoFilterExtension(None)

    def map_filter_field(self, filter_field: Filter) -> OpenApiTypes:
        if isinstance(filter_field, filters.DateFromToRangeFilter):
            return OpenApiTypes.DATE

        return self.extension.map_filter_field(filter_field)

    def get_choices(self, filter_field: Filter) -> list[str]:
        if isinstance(filter_field, filters.OrderingFilter):
            return [choice[0] for choice in filter_field.field.choices.choices]

        return []

    def get_fields(self, base_field: str, filter_field: Filter) -> list[str]:
        if type(filter_field) == filters.RangeFilter:
            return [base_field + "_min", base_field + "_max"]
        elif type(filter_field) == filters.DateFromToRangeFilter:
            return [base_field + "_after", base_field + "_before"]

        return [base_field]

    def get_field_description(self, field_name: str, filter_field: Filter) -> str:
        if type(filter_field) == filters.RangeFilter:
            if field_name.endswith("_min"):
                return RANGE_MIN_FILTER_DESC
            elif field_name.endswith("_max"):
                return RANGE_MAX_FILTER_DESC
            else:
                raise ValueError(f"Invalid RangeFilter field name {field_name}")
        elif type(filter_field) == filters.DateFromToRangeFilter:
            if field_name.endswith("_after"):
                return DATE_AFTER_FILTER_DESC
            elif field_name.endswith("_before"):
                return DATE_BEFORE_FILTER_DESC
            else:
                raise ValueError(f"Invalid RangeFilter field name {field_name}")

        return filter_field.extra.get('help_text')

    def get_param(self, base_field: str, filter_field: Filter) -> list[OpenApiParameter]:
        fields = self.get_fields(base_field, filter_field)
        choices = self.get_choices(filter_field)

        type_ = self.map_filter_field(filter_field)

        return [OpenApiParameter(field_name,
                                 type_,
                                 OpenApiParameter.QUERY,
                                 enum=choices,
                                 description=self.get_field_description(field_name,
                                                                        filter_field)
                                )
                for field_name in fields
               ]

ORDER_FILTER_DESC = ("Enable ordering. This filter is also "
                     "CSV-based, and accepts multiple ordering params")

DATE_AFTER_FILTER_DESC = "Discard rows before given date"
DATE_BEFORE_FILTER_DESC = "Discard rows after given date"
RANGE_MIN_FILTER_DESC = "Discard rows less then given value"
RANGE_MAX_FILTER_DESC = "Discard rows more then given value"
