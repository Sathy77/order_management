# Generated by Django 5.1.1 on 2024-10-29 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_transectionincome_transection'),
    ]

    operations = [
        migrations.AddField(
            model_name='transection',
            name='expense',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transectionexpense_expense', to='account.expense'),
        ),
        migrations.AlterField(
            model_name='transection',
            name='income',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transectionincome_income', to='account.income'),
        ),
    ]