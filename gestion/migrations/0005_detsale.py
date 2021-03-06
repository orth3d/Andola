# Generated by Django 3.0.3 on 2020-09-21 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0011_auto_20200921_0035'),
        ('gestion', '0004_auto_20200916_0058'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Producto')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.Sale')),
            ],
        ),
    ]
