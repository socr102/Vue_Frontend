import logging

from rest_framework import mixins, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import CustomUser
from backend.permissions import IsSuperUser, IsOwner, IsSuperUserOrAdmin

from .permissions import (UserModifyPermission,
                          CanDeactivateUserPermission,
                          CreateAndReadPermission,
                          UserReadPermission,
                          UserDeletePermission)
from .serializers import UserListSerializer, UserDetailSerializer, ChangePasswordSerializer
from .filters import UserListFilter

logger = logging.getLogger('django')

class UserList(generics.ListCreateAPIView):
    """List all snippets, or create a new snippet."""
    queryset = CustomUser.objects.all().select_related('created_by').\
        prefetch_related('groups')
    serializer_class = UserListSerializer
    permission_classes = [CreateAndReadPermission]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserListFilter


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """Retrieve, update a snippet instance."""
    queryset = CustomUser.objects.all().select_related('created_by')
    serializer_class = UserDetailSerializer
    permission_classes = [UserModifyPermission, UserReadPermission]

    _object = None

    def get_object(self):
        if self._object is None:
            self._object = super().get_object()
        return self._object

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [UserDeletePermission()]

        return [p() for p in self.permission_classes]

    def generic_method(self, method, request, *args, **kwargs):
        if IsSuperUserOrAdmin().has_permission(request, UserDetail):
            return method(request, *args, **kwargs)

        if request.user.id == kwargs['pk']:
            return method(request, *args, **kwargs)

        if request.user == self.get_object().created_by:
            return method(request, *args, **kwargs)

        raise PermissionDenied()

    def get(self, request, *args, **kwargs):
        return self.generic_method(self.retrieve, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.generic_method(self.update, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if request.data.get('is_superuser'):
            if IsSuperUser().has_permission(request, UserDetail):
                return self.partial_update(request, *args, **kwargs)
            else:
                raise PermissionDenied(detail='You can\'t update is_superuser field')

        return self.generic_method(self.partial_update, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ChangePassword(generics.UpdateAPIView):
    """Change own password by providing current user password."""
    queryset = CustomUser.objects.all()
    permission_classes = (IsOwner,)
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put']


class DeactivateUser(generics.DestroyAPIView):
    """Handle two-stage user deactivation process."""
    queryset = CustomUser.objects.all()
    permission_classes = (CanDeactivateUserPermission,)
    serializer_class = UserDetailSerializer

    def perform_destroy(self, instance):
        if instance.delete_request:
            instance.is_active = False
            logger.info(f"User.id={instance.id} is deactivated.")
        else:
            instance.delete_request = self.request.user
        instance.save()
        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.perform_destroy(self.get_object())
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
