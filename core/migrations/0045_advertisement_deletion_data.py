# Generated by Django 3.2.9 on 2022-01-11 18:37

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_advertisement_ad_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='deletion_data',
            field=models.DateField(default=core.models.get_30_days_ahead),
        ),
    ]
