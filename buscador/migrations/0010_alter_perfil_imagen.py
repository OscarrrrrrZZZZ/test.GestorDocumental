# Generated by Django 5.0.3 on 2024-06-12 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0009_alter_perfil_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='IMAGEN',
            field=models.ImageField(blank=True, default='perfiles/logo-default.png', null=True, upload_to='perfiles/'),
        ),
    ]
