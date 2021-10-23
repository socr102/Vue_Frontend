from django_filters.rest_framework import FilterSet, CharFilter

class AudienceFilter(FilterSet):
    """
    Attributes:
        name Filter by audience name
    """
    name = CharFilter(lookup_expr="trigram_similar")
