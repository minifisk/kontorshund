# Generated by Django 3.2.9 on 2022-01-09 16:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20220108_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsemail',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]