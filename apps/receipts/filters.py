from django.contrib.postgres.search import SearchVectorField, SearchQuery
from django.db.models.expressions import RawSQL
from django_filters.rest_framework import (DateFromToRangeFilter, CharFilter,
                                           FilterSet, OrderingFilter)

from .models import Article, Store, Receipt, OrderLine, Payment, Product
from .mixins import DateRangeMixin
from backend import utils

class ArticleFilter(DateRangeMixin, FilterSet):
    name = CharFilter(lookup_expr="trigram_similar", field_name="article__name")
    date = DateFromToRangeFilter(field_name="receipt__order_date")
    order = OrderingFilter(
        help_text=utils.ORDER_FILTER_DESC,
        fields = (
            ("sold_items", "sold_items")
        )
    )

    def full_text_search(self, queryset, name, value):
        queryset = queryset.annotate(
            ts=RawSQL(
                'textsearch',
                params=[],
                output_field=SearchVectorField()
            )
        ).filter(
            ts=value
        )

        return queryset

    class Meta:
        model = OrderLine
        fields = ['date']


class ProductFilter(DateRangeMixin, FilterSet):
    date = DateFromToRangeFilter(field_name="receipt__order_date")
    name = CharFilter(lookup_expr="trigram_similar", field_name="article__product__name")
    order = OrderingFilter(
        help_text=utils.ORDER_FILTER_DESC,
        fields = (
            ("sold_items", "sold_items")
        )
    )

    class Meta:
        model = OrderLine
        fields = ['date']


class StoreFilter(DateRangeMixin, FilterSet):
    date = DateFromToRangeFilter(field_name="receipt__order_date")
    order = OrderingFilter(
        help_text=utils.ORDER_FILTER_DESC,
        fields = (
            ("revenue", "revenue")
        )
    )
    class Meta:
        model = Payment
        fields = ['date']


class ReceiptFilter(DateRangeMixin, FilterSet):
    date = DateFromToRangeFilter(field_name="order_date")
    order = OrderingFilter(
        help_text=utils.ORDER_FILTER_DESC,
        fields = (
            ("order_date", "order_date")
        )
    )

    class Meta:
        model = Receipt
        fields = ['date']


class OrderFilter(DateRangeMixin, FilterSet):
    date = DateFromToRangeFilter(field_name="receipt__order_date")

    class Meta:
        model = OrderLine
        fields = ['date']


class PaymentDateFilter(DateRangeMixin, FilterSet):
    date = DateFromToRangeFilter(field_name="receipt__order_date")

    class Meta:
        model = Payment
        fields = ['date']
