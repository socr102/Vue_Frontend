from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import OfferFilter
from .models import Offer
from .permissions import OfferPermission
from .serializers import OfferSerializer
from backend.permissions import IsSuperUserOrAdmin


class OfferList(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter
    is_raised_err = False

    def get_queryset(self):
        if IsSuperUserOrAdmin().has_permission(self.request, OfferList):
            queryset = Offer.objects.all()
        else:
            queryset = Offer.objects.filter(
                organization=self.request.user.organization_id)

        return queryset.prefetch_related('articles')

    def finalize_response(self, request, response, *args, **kwargs):
        if self.request.user.is_authenticated and not self.is_raised_err:
            response['X-Total-Count'] = self.\
                    filter_queryset(self.get_queryset()).count()
        return super().finalize_response(request, response, *args, **kwargs)

    def handle_exception(self, exc):
        self.is_raised_err = True
        return super().handle_exception(exc)

    def head(self, request, *args, **kwargs):
        return Response({})


class OfferDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Offer.objects.all().select_related('created_by')
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated & OfferPermission]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
