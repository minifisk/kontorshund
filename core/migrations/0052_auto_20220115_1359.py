# Generated by Django 3.2.9 on 2022-01-15 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_province_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='municipality',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]