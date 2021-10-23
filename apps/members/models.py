from django.db import models

class Member(models.Model):
    SEX_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    external_id = models.CharField(max_length=64,
                                   help_text="ID from third party system")
    birth_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    organization = models.ForeignKey('organizations.Organization',
                                     on_delete=models.SET_NULL,
                                     null=True)
    store = models.ForeignKey('receipts.Store',
                              on_delete=models.SET_NULL,
                              null=True)
    sex = models.CharField(max_length=8,
                           choices=SEX_CHOICES,
                           default=SEX_CHOICES[0][0])

    class Meta:
        ordering = ['id']
