# Generated by Django 3.0.3 on 2020-10-21 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0007_auto_20201012_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='comment',
            field=models.CharField(blank=True, max_length=200, verbose_name='Comentarios'),
        ),
    ]
