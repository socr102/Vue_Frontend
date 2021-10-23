from django_filters.rest_framework import (DateFromToRangeFilter,
                                           FilterSet)
from .models import Article
from apps.receipts.mixins import DateRangeMixin

class TrendDateFilter(DateRangeMixin, FilterSet):
    date = DateFromToRangeFilter(required=True)

    class Meta:
        model = Article
        fields = ['date']
