# Generated by Django 5.1.1 on 2024-09-24 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_personal_phone_user_contact_no_user_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='personal_email',
        ),
    ]