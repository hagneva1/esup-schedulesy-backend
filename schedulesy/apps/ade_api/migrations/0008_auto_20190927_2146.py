# Generated by Django 2.1.12 on 2019-09-27 19:46

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ade_api', '0007_resource_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='events',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='localcustomization',
            name='customization_id',
            field=models.IntegerField(unique=True),
        ),
    ]
