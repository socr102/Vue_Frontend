from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class OrderLine(models.Model):
    article = models.ForeignKey('Article', on_delete=models.SET_NULL, null=True)
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE, related_name='orderline')
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey('members.Member', on_delete=models.SET_NULL, null=True)

    count = models.IntegerField(validators=[MinValueValidator(0)])
    # orderLine.itemPrice.currency
    currency = models.CharField(max_length=16)
    # orderLine.itemPrice.vat
    item_vat = models.FloatField(validators=[MinValueValidator(0.0)])
    # orderLine.itemPrice.value
    item_price = models.FloatField(validators=[MinValueValidator(0.0)])

    @staticmethod
    def get(order: dict, article, store, receipt, member):
        """
        @param orderLine: single order from storebox API
        @return: OrderLine object
        """
        return OrderLine(receipt=receipt,
                         store=store,
                         member=member,
                         article=article,
                         currency=order['itemPrice']['currency'],
                         item_vat=order['itemPrice']['vat'],
                         item_price=order['itemPrice']['value'],
                         count=order['count'])

    @classmethod
    def make_anonymous(cls, member_id):
        """Make member orders anonymous."""
        return cls.objects.filter(member_id=member_id).update(member=None)
