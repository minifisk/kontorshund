# Generated by Django 3.2.9 on 2022-03-01 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_newsemail_interval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsemail',
            name='ad_type',
            field=models.CharField(choices=[('eeee', 'ffff'), ('gggg', 'hhhh')], default='eeee', max_length=10, verbose_name='Annonstyp'),
        ),
        migrations.AlterField(
            model_name='newsemail',
            name='interval',
            field=models.CharField(choices=[('aaaa', 'bbbb'), ('cccc', 'dddd')], default='aaaa', max_length=10, verbose_name='Intervall'),
        ),
    ]