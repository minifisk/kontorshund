# Generated by Django 3.2.9 on 2021-12-30 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_rename_breed_advertisement_hundras'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.province'),
        ),
    ]