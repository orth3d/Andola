# Generated by Django 3.0.3 on 2021-01-08 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_auto_20201027_1109'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
