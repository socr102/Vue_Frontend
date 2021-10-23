from django_filters.rest_framework import BooleanFilter, FilterSet, CharFilter

from .models import CustomUser
from .serializers import GroupsSerializer
from backend.settings import MERCHANT_ADMIN, MERCHANT_WORKER


class UserListFilter(FilterSet):
    superadmin = BooleanFilter(field_name='is_superuser')
    admin = BooleanFilter(field_name='is_staff')
    merchant = BooleanFilter(method='merchant_filter')
    worker = BooleanFilter(method='worker_filter')

    class Meta:
        model = CustomUser
        fields = ['superadmin', 'admin', 'organization', 'merchant', 'worker']

    def merchant_filter(self, queryset, name, value):
        if not value:
            return queryset.exclude(groups__name=MERCHANT_ADMIN)

        return queryset.filter(groups__name=MERCHANT_ADMIN)

    def worker_filter(self, queryset, name, value):
        if not value:
            return queryset.exclude(groups__name=MERCHANT_WORKER)

        return queryset.filter(groups__name=MERCHANT_WORKER)

    @property
    def qs(self):
        parent = super(UserListFilter, self).qs
        if self.request.user.groups.filter(name=MERCHANT_ADMIN).exists():
            return parent.filter(created_by=self.request.user.id)
        return parent
