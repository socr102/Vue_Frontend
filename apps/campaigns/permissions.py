from rest_framework.permissions import BasePermission

class CampaignPermission(BasePermission):
    UPD_METHODS = ['PATCH', 'PUT']

    def has_object_permission(self, request, view, campaign):
        if request.method in self.UPD_METHODS:
            if campaign.offer.is_active: return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        if campaign.organization_id == request.user.organization_id:
            return True

        return False
