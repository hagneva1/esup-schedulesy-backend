# Generated by Django 2.1.12 on 2019-09-24 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ade_api', '0004_localcustomization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localcustomization',
            name='username',
            field=models.CharField(blank=True, db_column='uid', max_length=32, unique=True),
        ),
    ]
