# Generated by Django 5.0.3 on 2024-06-17 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0018_archivo_fecha_carga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='FECHA_CARGA',
            field=models.DateField(auto_now_add=True),
        ),
    ]