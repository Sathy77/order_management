# Generated by Django 5.1.1 on 2024-11-07 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_quntity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quntity',
            field=models.IntegerField(default=0),
        ),
    ]
