from rest_framework.permissions import BasePermission


class AudiencePermission(BasePermission):
    def has_object_permission(self, request, view, audience):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if audience.organization_id == request.user.organization_id:
            return True

        return False
