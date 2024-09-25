# Generated by Django 5.1.1 on 2024-09-25 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_ordersummary_grand_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersummary',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('Cash on Delivery', 'Cash on Delivery'), ('Credit/Debit Card', 'Credit/Debit Card'), ('Mobile Wallet', 'Mobile Wallet')], default='Cash on Delivery', max_length=20, null=True),
        ),
    ]
