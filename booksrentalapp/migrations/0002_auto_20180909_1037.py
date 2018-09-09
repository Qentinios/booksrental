# Generated by Django 2.1.1 on 2018-09-09 08:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('booksrentalapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='rent_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date rented'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rent',
            name='return_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='date returned'),
        ),
    ]
