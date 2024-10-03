# Generated by Django 5.1.1 on 2024-09-30 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_created_by_alter_user_updated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Customer', 'Customer')], default='Customer', max_length=25),
        ),
    ]