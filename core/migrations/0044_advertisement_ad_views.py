# Generated by Django 3.2.9 on 2022-01-10 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_alter_newsemail_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='ad_views',
            field=models.IntegerField(default=0),
        ),
    ]
