# Generated by Django 3.2.9 on 2021-12-19 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_advertisement_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='payment_type',
            field=models.CharField(choices=[('S', 'Swish'), ('B', 'Bankgiro')], default=1, max_length=1, verbose_name='Betalningsmetod'),
        ),
    ]
