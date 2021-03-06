# Generated by Django 3.0.3 on 2020-10-13 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0006_auto_20200930_1154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detsale',
            options={'ordering': ['id'], 'verbose_name': 'Detalle de Venta', 'verbose_name_plural': 'Detalle de Ventas'},
        ),
        migrations.AddField(
            model_name='detsale',
            name='subcosto',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='sale',
            name='costo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
