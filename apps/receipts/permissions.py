from apps.receipts.models.receipt import Receipt
from rest_framework.permissions import BasePermission

from .models import Receipt

class ReceiptPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        return obj['organization_id'] == request.user.organization_id
