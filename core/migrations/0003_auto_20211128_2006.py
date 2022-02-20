# Generated by Django 3.2.9 on 2021-11-28 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_municipality_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='days_per_week',
            field=models.CharField(choices=[('1', '1 day per week'), ('1-5', '1-2 days per week'), ('1-3', '1-3 days per week'), ('1-4', '1-4 days per week'), ('1-5', '1-5 days per week')], default=1, max_length=3),
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.municipality')),
            ],
        ),
    ]
