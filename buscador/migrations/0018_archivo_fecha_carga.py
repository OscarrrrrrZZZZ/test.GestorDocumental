# Generated by Django 5.0.3 on 2024-06-17 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0017_perfil_uo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivo',
            name='FECHA_CARGA',
            field=models.DateField(default='1900-01-01'),
        ),
    ]
