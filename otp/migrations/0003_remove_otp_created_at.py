# Generated by Django 5.1.1 on 2024-11-06 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0002_alter_otp_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='created_at',
        ),
    ]
