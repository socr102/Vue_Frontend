from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        MASTERCARD = 'MASTERCARD', _('MASTERCARD')
        VISA = 'VISA', _('VISA')
        CACH = 'CACH', _('CACH')
        INVOICE = 'INVOICE', _('INVOICE')

    payment_type = models.CharField(
        max_length=64,
        choices=PaymentType.choices
    )
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    currency = models.CharField(max_length=16)
    truncated_card_number = models.CharField(max_length=16)
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE, null=True)

    @staticmethod
    def get(payment: dict, receipt):
        """
        @param payment: payment data from storebox API
        @return: Payment object
        """
        return Payment(receipt=receipt,
                       currency=payment['priceCurrency'],
                       payment_type=payment['paymentType'],
                       truncated_card_number=payment['truncatedCardNumber'],
                       price=payment['priceValue'])


