# Generated by Django 3.2.9 on 2021-12-04 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_advertisement_breed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='breed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.dogbreeds', verbose_name='Hundras'),
        ),
    ]
