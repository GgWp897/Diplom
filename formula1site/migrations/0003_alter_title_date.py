# Generated by Django 5.0.2 on 2024-05-12 22:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula1site', '0002_alter_title_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
    ]
