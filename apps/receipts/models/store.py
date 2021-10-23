from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import Coalesce

from apps.receipts.managers import StoreManager
import apps.receipts.models as models_

class Store(models.Model):
    name = models.CharField(max_length=255)  # store.storeName
    address = models.CharField(max_length=255)  # store.storeAddressLine1
    external_id = models.CharField(max_length=255)  # store.storeId
    reg_number = models.CharField(max_length=255)  # store.storeRegNumber
    zipcode = models.CharField(max_length=255)  # store.storeZipCode
    country = models.CharField(max_length=255)  # store.storeCountry
    city = models.CharField(max_length=255)  # store.storeCity
    phone = models.CharField(max_length=255)  # store.storePhone
    merchant = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True)
    objects = StoreManager()

    class Meta:
        unique_together = ('name', 'address',)

    def __hash__(self):
        return hash(self.name + self.address)

    def __eq__(self, other):
        return (self.name + self.address) ==\
               (other.name + other.address)

    @staticmethod
    def get(store: dict, merchant):
        """
        @param store: store data from storebox API
        @return: Store object
        """
        return Store(name=store['storeName'],
                     address=store['storeAddressLine1'],
                     external_id=store['storeId'],
                     reg_number=store['storeRegNumber'],
                     zipcode=store['storeZipCode'],
                     country=store['storeCountry'],
                     city=store['storeCity'],
                     phone=store['storePhone'],
                     merchant=merchant)

    @staticmethod
    def list_items(user):
        # use Payment model to avoid spanning multi-valued relationships
        # https://docs.djangoproject.com/en/dev/topics/db/queries/#spanning-multi-valued-relationships
        return models_.Payment.objects \
            .filter(receipt__orderline__store__merchant__isnull=False,
                    receipt__orderline__store__isnull=False,
                    receipt__orderline__store__merchant__organization_id=user.organization_id) \
            .values('receipt__orderline__store_id') \
            .annotate(revenue=Coalesce(Sum('price'), 0))

    @staticmethod
    def item_values(qs: QuerySet):
        return qs.values('receipt__orderline__store_id',
                         'receipt__orderline__store__name',
                         'receipt__orderline__store__address',
                         'revenue')
