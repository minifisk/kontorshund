# Generated by Django 3.2.9 on 2021-11-30 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20211128_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='area',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.area'),
            preserve_default=False,
        ),
    ]
