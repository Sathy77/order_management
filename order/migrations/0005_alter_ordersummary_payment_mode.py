# Generated by Django 5.1.1 on 2024-09-26 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_ordersummary_payment_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersummary',
            name='payment_mode',
            field=models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Credit/Debit Card', 'Credit/Debit Card'), ('Mobile Wallet', 'Mobile Wallet')], default='Cash on Delivery', max_length=25),
        ),
    ]
