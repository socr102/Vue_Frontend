from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from django.http import Http404
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .models import Store, Article, OrderLine, Payment, Product, Receipt
from .permissions import ReceiptPermission
from backend.permissions import (IsSuperUserOrAdmin,
                                 IsOwnerOrAdminStoreModel)

from .serializers import (StoreSerializer,
                          FetchStoreSerializer,
                          ArticleSerializer,
                          FetchArticleSerializer,
                          OrderLineSerializer,
                          OrderLineDetailSerializer,
                          PaymentSerializer,
                          ProductSerializer,
                          FetchProductSerializer,
                          ArticlesRecSerializer,
                          ProductConnectionSerializer,
                          ArticleConnectionSerializer,
                          ProdRecInputSerializer,
                          ArticleRecInputSerializer,
                          ProductRecSerializer,
                          ArticleBoughtTogetherSerializer)

from .filters import (ArticleFilter, PaymentDateFilter,
                      StoreFilter, OrderFilter, ProductFilter)
from .schema import list_article_recs_schema, list_product_recs_schema
from backend.schema import list_schema


@list_schema(StoreFilter)
class StoreList(generics.ListAPIView):
    """List all snippets, or create a new snippet."""
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StoreFilter
    is_raised_err = False

    def head(self, request, *args, **kwargs):
        return Response({})

    def get_queryset(self):
        return Store.list_items(self.request.user)

    def handle_exception(self, exc):
        self.is_raised_err = True
        return super().handle_exception(exc)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = Store.item_values(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FetchStoreSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FetchStoreSerializer(queryset, many=True)
        return Response(serializer.data)

    def finalize_response(self, request, response, *args, **kwargs):
        if self.request.user.is_authenticated and not self.is_raised_err:
            response['X-Total-Count'] = self.get_queryset().count()
        return super().finalize_response(request, response, *args, **kwargs)


class StoreDetail(viewsets.ModelViewSet):
    """Retrieve, update or delete a snippet instance."""
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsOwnerOrAdminStoreModel]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if IsSuperUserOrAdmin:
            return self.destroy(request, *args, **kwargs)


@list_schema(ArticleFilter)
class ArticleList(generics.ListAPIView):
    """List all snippets, or create a new snippet."""
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter

    def get_queryset(self):
        return Article.list_items(self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = Article.item_values(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FetchArticleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FetchArticleSerializer(queryset, many=True)
        return Response(serializer.data)


@list_schema(OrderFilter)
class OrderList(generics.ListAPIView):
    """List all snippets, or create a new snippet."""
    serializer_class = OrderLineSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter
    is_raised_err = False

    def get_queryset(self):
        return OrderLine.objects.filter(
            store__merchant__organization_id=self.request.user.organization_id)

    def handle_exception(self, exc):
        self.is_raised_err = True
        return super().handle_exception(exc)

    def finalize_response(self, request, response, *args, **kwargs):
        if self.request.user.is_authenticated and not self.is_raised_err:
            response['X-Total-Count'] = self.filter_queryset(self.get_queryset()).count()
        return super().finalize_response(request, response, *args, **kwargs)

    def head(self, request, *args, **kwargs):
        return Response({})


@list_schema(PaymentDateFilter)
class PaymentList(generics.ListAPIView):
    """List all snippets, or create a new snippet."""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentDateFilter
    is_raised_err = False

    def get_queryset(self):
        ids = OrderLine.objects.filter(
                store__merchant__organization_id=self.request.user.organization_id
            ).values_list('receipt_id', flat=True)
        return Payment.objects.filter(receipt_id__in=ids)

    def handle_exception(self, exc):
        self.is_raised_err = True
        return super().handle_exception(exc)

    def finalize_response(self, request, response, *args, **kwargs):
        if self.request.user.is_authenticated and not self.is_raised_err:
            response['X-Total-Price'] = int(
                self.filter_queryset(self.get_queryset()).\
                    aggregate(price__sum=Coalesce(Sum('price'), 0))
                    ['price__sum'])
        return super().finalize_response(request, response, *args, **kwargs)

    def head(self, request, *args, **kwargs):
        return Response({})


@list_schema(ProductFilter)
class ProductList(generics.ListAPIView):
    """List all snippets, or create a new snippet."""
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.list_items(self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = Product.item_values(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FetchProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FetchProductSerializer(queryset, many=True)
        return Response(serializer.data)


@list_article_recs_schema
class ArticleRecommendations(generics.ListAPIView):
    """Get articles bought together with a given list of articles."""
    serializer_class = ArticlesRecSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        flt = ArticleRecInputSerializer(data=self.request.GET)
        flt.is_valid(raise_exception=True)
        return Article.recommendations(flt.validated_data['article'],
                                       self.request.user.organization_id)


class ConnectedProducts(generics.ListAPIView):
    """Get strongly connected products.
    Products which bought often together.
    """
    serializer_class = ProductConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.find_connections(self.request.user.organization_id)

    @method_decorator(cache_page(60*5))
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@list_product_recs_schema
class ConnectedArticles(generics.ListAPIView):
    """Fetches strongly connected articles.
    Articles which bought often together.
    """
    serializer_class = ArticleConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Article.find_connections(self.request.user.organization_id,
                                        self.request.GET.getlist('product'))

@list_product_recs_schema
class BoughtTogetherArticles(generics.ListAPIView):
    """Fetches strongly connected articles to the list of articles.
    Articles which bought often together.
    Split by products(categories).
    """
    serializer_class = ArticleBoughtTogetherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Article.bought_together(self.request.user.organization_id,
                                       self.request.GET.getlist('article'))



@list_product_recs_schema
class ProductRecommendations(generics.ListAPIView):
    """Get products bought together with a given list of products."""
    serializer_class = ProductRecSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        flt = ProdRecInputSerializer(data=self.request.GET)
        flt.is_valid(raise_exception=True)
        return Product.recommendations(flt.validated_data['product'],
                                       self.request.user.organization_id)


class ReceiptOrdersList(generics.GenericAPIView):
    serializer_class = OrderLineDetailSerializer
    permission_classes = [permissions.IsAuthenticated & ReceiptPermission]

    def get_object(self, pk):
        obj = Receipt.objects.filter(pk=pk, orderline__store__merchant__isnull=False).\
            prefetch_related('orderline__store__merchant').\
            values(organization_id=F('orderline__store__merchant__organization_id')).\
            first()

        if not obj:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        receipt_id = self.kwargs.get('pk')
        return OrderLine.objects.filter(receipt_id=receipt_id) \
                        .select_related('store', 'article')

    def get(self, request, *args, **kwargs):
        self.get_object(self.kwargs.get('pk'))
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
