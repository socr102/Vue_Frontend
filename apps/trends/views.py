from rest_framework import mixins, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Trend
from .serializers import ArticleTrendSerializer, ProductTrendSerializer
from .filters import TrendDateFilter
from .schema import trend_schema
from .utils import DIRECTIONS
from backend.schema import list_schema

class ArticleTrends(APIView):
    """Returns trending articles for selected period."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleTrendSerializer

    @list_schema(TrendDateFilter)
    @trend_schema
    def get(self, request, direction):
        if direction not in DIRECTIONS:
            raise ValidationError({"direction": "Invalid trend direction"})

        flt = TrendDateFilter(request.GET)
        if not flt.is_valid():
            raise ValidationError(flt.errors)

        trends = Trend.trending_articles(flt.form.cleaned_data['date'].start,
                                         flt.form.cleaned_data['date'].stop,
                                         direction, request.user.organization_id)

        serializer = ArticleTrendSerializer(trends, many=True)
        return Response(serializer.data)


class ProductTrends(APIView):
    """Returns trending products for selected period."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductTrendSerializer

    @list_schema(TrendDateFilter)
    @trend_schema
    def get(self, request, direction):
        if direction not in DIRECTIONS:
            raise ValidationError({"direction": "Invalid trend direction"})

        flt = TrendDateFilter(request.GET)
        if not flt.is_valid():
            raise ValidationError(flt.errors)

        trends = Trend.trending_products(flt.form.cleaned_data['date'].start,
                                         flt.form.cleaned_data['date'].stop,
                                         direction, request.user.organization_id)

        serializer = ProductTrendSerializer(trends, many=True)
        return Response(serializer.data)
