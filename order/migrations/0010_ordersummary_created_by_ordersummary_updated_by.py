# Generated by Django 5.1.1 on 2024-10-22 07:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_ordersummary_payment_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersummary',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordersummary_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ordersummary',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordersummary_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
