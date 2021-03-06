# Generated by Django 3.0.3 on 2020-09-30 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0011_auto_20200921_0035'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdServ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('categoria', models.CharField(choices=[('P', 'Producto'), ('S', 'Servicio')], default='P', max_length=1)),
                ('thumbnail', models.FileField(upload_to='', verbose_name='Imagen')),
                ('precio', models.FloatField(default=0)),
                ('costo', models.FloatField(default=0, verbose_name='Costo Unitario')),
                ('cantidad_almacen', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='producto',
            name='categoria',
        ),
        migrations.DeleteModel(
            name='Servicio',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
