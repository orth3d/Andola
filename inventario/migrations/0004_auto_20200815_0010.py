# Generated by Django 3.0.3 on 2020-08-15 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_auto_20200814_2336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='categoria',
            new_name='catego',
        ),
    ]
