from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula1site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата'),
        ),
    ]
