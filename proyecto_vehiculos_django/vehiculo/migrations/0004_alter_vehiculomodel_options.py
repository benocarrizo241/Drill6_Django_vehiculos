# Generated by Django 4.0.5 on 2023-08-06 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0003_alter_vehiculomodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehiculomodel',
            options={'permissions': [('visualizar_catalogo', 'Puede visualizar_catalogo'), ('add', 'Puede agregar vehiculos')]},
        ),
    ]