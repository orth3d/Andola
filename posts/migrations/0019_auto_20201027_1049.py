# Generated by Django 3.0.3 on 2020-10-27 16:49

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_auto_20201027_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='overview',
            field=tinymce.models.HTMLField(max_length=200, verbose_name='Descripción'),
        ),
    ]
