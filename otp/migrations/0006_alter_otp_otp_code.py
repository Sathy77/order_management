# Generated by Django 5.1.1 on 2024-11-07 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0005_alter_otp_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp_code',
            field=models.CharField(max_length=10),
        ),
    ]
