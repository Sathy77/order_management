# Generated by Django 5.1.1 on 2024-11-17 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_storeorderid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersummary',
            name='order_note',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]