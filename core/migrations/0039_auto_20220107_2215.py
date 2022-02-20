# Generated by Django 3.2.9 on 2022-01-07 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0038_auto_20220107_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsemail',
            name='areas',
            field=models.ManyToManyField(blank=True, to='core.Area', verbose_name='Område'),
        ),
        migrations.AlterField(
            model_name='newsemail',
            name='interval',
            field=models.IntegerField(blank=True, choices=[(1, 'Veckovis'), (2, 'Dagligen')], null=True),
        ),
        migrations.AlterField(
            model_name='newsemail',
            name='municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.municipality', verbose_name='Kommun'),
        ),
        migrations.AlterField(
            model_name='newsemail',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.province', verbose_name='Landskap'),
        ),
        migrations.AlterField(
            model_name='newsemail',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
