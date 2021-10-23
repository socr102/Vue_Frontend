from django_filters.rest_framework import (
    FilterSet, CharFilter, BooleanFilter,
    OrderingFilter, DateTimeFilter
)
from django.db.models import F
from django.conf import settings

from .models import Campaign
from apps.offers.utils import Q_is_active_offer, Q_is_archive_offer
from backend import utils

START_DATE = "offer__start_date"
END_DATE = "offer__end_date"
DATE_FORMATS = settings.REST_FRAMEWORK['DATETIME_INPUT_FORMATS']

class CampaignOrderingFilter(OrderingFilter):

    __field = 'metadata__' + Campaign.REVENUE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('revenue', 'Revenue'),
            ('-revenue', 'Revenue (descending)'),
        ]
        self.extra['help_text'] = utils.ORDER_FILTER_DESC

    def filter(self, qs, value):
        # OrderingFilter is CSV-based, so `value` is a ist
        if value and any(v in ['revenue', '-revenue'] for v in value):
            F_EXPR = F(self.__field)
            if value[0].startswith('-'):
                F_EXPR = F_EXPR.desc(nulls_last=True)
            else:
                F_EXPR = F_EXPR.asc(nulls_first=True)
            return qs.order_by(F_EXPR)

        return super().filter(qs, value)


class CampaignFilter(FilterSet):
    name = CharFilter(lookup_expr="trigram_similar")
    is_active = BooleanFilter(method='active', help_text="Filter by campaign active status")
    is_archive = BooleanFilter(method='archive', help_text="Filter by campaign finish status")
    order = CampaignOrderingFilter()

    date_after = DateTimeFilter(field_name=START_DATE,
                                lookup_expr="gte",
                                input_formats=DATE_FORMATS,
                                help_text=utils.DATE_AFTER_FILTER_DESC)
    date_before = DateTimeFilter(field_name=END_DATE,
                                 lookup_expr="lte",
                                 input_formats=DATE_FORMATS,
                                 help_text=utils.DATE_BEFORE_FILTER_DESC)

    class Meta:
        model = Campaign
        fields = ['name', 'is_active', 'is_archive',
                  'date_after', 'date_before']

    def active(self, queryset, name, value):
        q = Q_is_active_offer(value, START_DATE, END_DATE)
        return queryset.filter(q)

    def archive(self, queryset, name, value):
        q = Q_is_archive_offer(value, END_DATE)
        return queryset.filter(**q)
