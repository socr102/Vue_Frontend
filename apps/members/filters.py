from django.contrib.postgres.search import SearchVectorField
from django.db.models.expressions import RawSQL
from django.db.models import Q
from django_filters.rest_framework import (FilterSet,
                                           CharFilter,
                                           RangeFilter,
                                           BooleanFilter,
                                           NumberFilter)

from datetime import datetime


class MemberFilter(FilterSet):
    q = CharFilter(method="full_text_search", help_text="Filter by members name, phone, email")
    sex = CharFilter(help_text="Filter by members name, phone, email")
    age = RangeFilter(method="age_filter")
    pref = NumberFilter(method="pref_filter",
                        help_text=("Filter by members article preferences."
                                   " Accepts multiple params"))
    is_active = BooleanFilter()

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

    def age_filter(self, queryset, name, value):
        today = datetime.today()
        if value.stop:
            from_date = today.replace(year=today.year - value.stop)
            queryset = queryset.filter(birth_date__gte=from_date)
        if value.start:
            to_date = today.replace(year=today.year - value.start)
            queryset = queryset.filter(birth_date__lte=to_date)

        return queryset

    def pref_filter(self, queryset, name, value):
        prefs = self.request.GET.getlist(name)

        q_objects = Q()
        for p in prefs:
            # 'and' the Q objects together
            q_objects &= Q(orderline__article=p)

        return queryset.filter(q_objects).distinct('id')
