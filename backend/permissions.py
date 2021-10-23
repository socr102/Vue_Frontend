from rest_framework.permissions import BasePermission

INFO_METHODS = ('HEAD', 'OPTIONS')


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSuperUserOrAdmin(BasePermission):
    """
    Allows access only to super users or admins
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser or request.user.is_staff)


class IsOwnerOrAdminUserModel(BasePermission):
    """
    Custom permission to only allow owners or admins of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in INFO_METHODS:
            return True
        return obj == request.user or request.user.is_staff or request.user.is_superuser


class IsOwnerOrAdminStoreModel(BasePermission):
    """
    Custom permission to only allow owners or admins of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in INFO_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if request.method in ('GET', 'POST', 'PUT', 'PATCH'):
            return obj == request.user or request.user.is_staff


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in INFO_METHODS:
            return True
        return obj == request.user


class IsMerchant(BasePermission):
    """
    Custom permission to only allow merchants to access resource.
    """

    def has_permission(self, request, view):
        return request.user.is_merchant
