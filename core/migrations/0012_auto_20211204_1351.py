# Generated by Django 3.2.9 on 2021-12-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20211204_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='DogBreeds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='size_requested',
            field=models.ManyToManyField(related_name='size_requested', to='core.DogSizeChoices', verbose_name='Möjliga hundstorlekar'),
        ),
    ]
