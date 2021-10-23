from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from rest_framework import generics, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .filters import AudienceFilter
from .models import Audience
from .serializers import AudienceSerializer
from .permissions import AudiencePermission
from backend.permissions import IsSuperUserOrAdmin
import apps.members.models as member_model


class AudienceList(generics.ListCreateAPIView):
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AudienceFilter

    def get_queryset(self):
        if IsSuperUserOrAdmin().has_permission(self.request, AudienceList):
            queryset = Audience.objects.all()
        else:
            queryset = Audience.objects.filter(
                organization=self.request.user.organization_id)

        return queryset.prefetch_related(Prefetch(
            'members',
            queryset=member_model.Member.objects.all().only('id')))

class AudienceDetail(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer
    permission_classes = [IsAuthenticated & AudiencePermission]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

