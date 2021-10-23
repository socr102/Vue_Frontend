from rest_framework.permissions import BasePermission

class MemberPermission(BasePermission):

    def has_object_permission(self, request, view, member):
        if request.method == 'DELETE':
            if not member.is_active: return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        if member.organization_id == request.user.organization_id:
            return True

        return True


class BaseMemberPermission(BasePermission):

    def has_permission(self, request, view):
        return False