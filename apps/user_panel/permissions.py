from rest_framework.permissions import BasePermission


class CreateAndReadPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        if request.user.groups.filter(name='merchant'):
            return True


class UserModifyPermission(BasePermission):
    METHODS_TO_CHECK = ['POST', 'PUT', 'PATCH']

    def has_permission(self, request, view):
        if request.method not in self.METHODS_TO_CHECK:
            return True

        if request.user.is_superuser:
            return True

        user = view.get_object()
        if user.is_superuser or user.is_staff:
            return False

        return True


class UserReadPermission(BasePermission):
    METHODS_TO_CHECK = ['GET']

    def has_permission(self, request, view):
        if request.method not in self.METHODS_TO_CHECK:
            return True

        if request.user.is_superuser:
            return True

        if request.data.get('is_superuser') or request.data.get('is_staff'):
            return False

        return True


class CanDeactivateUserPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_staff and not request.user.is_superuser:
            # merchant users don't have rights
            # to deactivate another user
            return False

        if not obj.is_active:
            # user already deactivated
            return False

        if obj.delete_request == request.user:
            # can't confirm action by the same user
            return False

        if request.user.is_superuser:
            return True

        if obj.delete_request is not None:
            # only superuser can confirm deactivation
            return False

        if obj.is_staff or obj.is_superuser:
            # only superuser can deactivate staff
            return False

        return True


class UserDeletePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            # can't to deactivate self
            return False

        if obj.is_merchant:
            # can't to deactivate merchant
            return False

        if request.user.is_superuser:
            return True

        if obj.is_staff or obj.is_superuser:
            # only superuser can deactivate staff
            return False

        if not request.user.is_staff and obj.created_by != request.user:
            return False

        return True
