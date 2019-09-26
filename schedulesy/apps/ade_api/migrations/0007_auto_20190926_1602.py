# Generated by Django 2.1.12 on 2019-09-26 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ade_api', '0006_resource_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ade_api.Resource'),
        ),
    ]
