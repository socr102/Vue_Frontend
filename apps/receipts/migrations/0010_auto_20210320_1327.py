# Generated by Django 3.1.3 on 2021-03-20 13:27

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0009_auto_20210228_1331'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='article',
            index=django.contrib.postgres.indexes.GistIndex(fields=['name'], name='article_trgm_idx', opclasses=('gist_trgm_ops',)),
        ),
    ]
