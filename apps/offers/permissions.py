from rest_framework.permissions import BasePermission


class OfferPermission(BasePermission):
    UPD_METHODS = ['PATCH', 'PUT']

    def has_object_permission(self, request, view, offer):
        if request.method in self.UPD_METHODS:
            if offer.is_active: return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        if offer.organization_id == request.user.organization_id:
            return True

        return False
