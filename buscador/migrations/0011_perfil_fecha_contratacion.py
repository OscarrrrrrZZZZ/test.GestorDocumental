# Generated by Django 5.0.3 on 2024-06-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0010_alter_perfil_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='FECHA_CONTRATACION',
            field=models.DateField(default='1900-01-01'),
        ),
    ]