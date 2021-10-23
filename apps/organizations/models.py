from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "organizations"
