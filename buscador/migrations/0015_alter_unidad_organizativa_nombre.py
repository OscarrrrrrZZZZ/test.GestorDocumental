# Generated by Django 5.0.3 on 2024-06-12 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0014_unidad_organizativa_remove_perfil_fecha_contratacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unidad_organizativa',
            name='NOMBRE',
            field=models.CharField(max_length=255),
        ),
    ]