# Generated by Django 3.1.3 on 2021-01-24 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_auto_20210120_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='is_archive',
        ),
    ]
