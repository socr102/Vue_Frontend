# Generated by Django 3.1.3 on 2021-01-22 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('receipts', '0004_product_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.member'),
        ),
    ]
