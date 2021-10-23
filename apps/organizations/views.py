from rest_framework import viewsets

from backend.permissions import IsSuperUserOrAdmin, IsMerchant
from .models import Organization
from .serializers import OrgSerializer

class OrgViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrgSerializer
    permission_classes = [IsSuperUserOrAdmin | IsMerchant]

    def get_queryset(self):
        if self.request.user.is_merchant:
            return [Organization.objects.get(id=self.request.user.organization_id)]
        return Organization.objects.all()
