# Generated by Django 5.1.1 on 2024-10-31 10:20

import django.db.models.deletion
import helps.abstract.abstractclass
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_role_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissioncategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(default=helps.abstract.abstractclass.generate_unique_code, editable=False, max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='role',
            name='permission',
            field=models.ManyToManyField(blank=True, to='user.permission'),
        ),
        migrations.AddField(
            model_name='permission',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.permissioncategory'),
        ),
    ]
