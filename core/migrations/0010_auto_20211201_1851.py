# Generated by Django 3.2.9 on 2021-12-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_advertisement_breed'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
