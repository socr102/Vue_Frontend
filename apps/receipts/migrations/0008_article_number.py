# Generated by Django 3.1.3 on 2021-02-24 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0007_auto_20210213_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='number',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
