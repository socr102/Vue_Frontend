# Generated by Django 3.1.3 on 2020-12-07 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('receipts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='merchant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='receipt',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='receipts.payment'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipts.store'),
        ),
        migrations.AddField(
            model_name='orderline',
            name='articles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='receipts.article'),
        ),
        migrations.AddField(
            model_name='orderline',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipts.receipt'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='articles',
            field=models.ManyToManyField(to='receipts.Article'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='receipts.productcategory'),
        ),
    ]