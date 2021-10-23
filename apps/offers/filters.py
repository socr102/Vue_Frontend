from django.conf import settings
from django_filters.rest_framework import (
    BooleanFilter, FilterSet, CharFilter, DateTimeFilter)

from .models import Offer
from .utils import Q_is_active_offer, Q_is_archive_offer

DATE_FORMATS = settings.REST_FRAMEWORK['DATETIME_INPUT_FORMATS']

class OfferFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr="trigram_similar")
    is_active = BooleanFilter(method='active')
    is_archive = BooleanFilter(method='archive')
    date_after = DateTimeFilter(field_name='start_date',
                                lookup_expr="gte",
                                input_formats=DATE_FORMATS)
    date_before = DateTimeFilter(field_name='end_date',
                                 lookup_expr="lte",
                                 input_formats=DATE_FORMATS)

    class Meta:
        model = Offer
        fields = ['name',
                  'is_active',
                  'is_archive',
                  'date_before',
                  'date_after'
                  ]

    def active(self, queryset, name, value):
        q = Q_is_active_offer(value)
        return queryset.filter(q)

    def archive(self, queryset, name, value):
        q = Q_is_archive_offer(value)
        return queryset.filter(**q)
