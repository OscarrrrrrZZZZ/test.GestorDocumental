from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subCarpetas', null=True, blank=True)

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='Archivos')

    def __str__(self):
        return self.name
    
class UNIDAD_ORGANIZATIVA(models.Model):
    id = models.AutoField(primary_key=True)
    NOMBRE = models.CharField(max_length=255)

    def __str__(self):
        return self.NOMBRE
    
class REPOSITORIO(models.Model):
    id = models.AutoField(primary_key=True)
    NOMBRE = models.CharField(max_length=255)

    def __str__(self):
        return self.NOMBRE
    
class PERFIL(models.Model):
    id = models.IntegerField(primary_key=True)
    NOMBRES = models.CharField(max_length=255)
    APELLIDO_PATERNO = models.CharField(max_length=255)
    APELLIDO_MATERNO = models.CharField(max_length=255)
    ACTIVO = models.BooleanField(default=True)
    IMAGEN = models.ImageField(upload_to='perfiles/',null=True, blank=True, default='perfiles/logo-default.png')
    FECHA_CONTRATACION = models.DateField(null=False, default='1900-01-01')
    UO_ID = models.ForeignKey(UNIDAD_ORGANIZATIVA, on_delete=models.CASCADE, related_name='subCarpeta', null=False, blank=True, default=1)
    
    def __str__(self):
        return f"{self.NOMBRES} {self.APELLIDO_PATERNO} {self.APELLIDO_MATERNO}"

class CARPETA(models.Model):
    id = models.AutoField(primary_key=True)
    NOMBRE = models.CharField(max_length=255)
    ID_PERFIL = models.ForeignKey(PERFIL, on_delete=models.CASCADE, related_name='subCarpeta', null=False, blank=True)
    
    def __str__(self):
        return self.NOMBRE

class ARCHIVO(models.Model):
    id = models.AutoField(primary_key=True)
    NOMBRE = models.CharField(max_length=255)
    ARCHIVO = models.FileField(upload_to='archivos/', null=True, blank=True)
    MASIVA = models.BooleanField(default=False)
    FECHA_CARGA = models.DateField(auto_now_add=True, null=False)
    ID_CARPETA = models.ForeignKey(CARPETA, on_delete=models.CASCADE, related_name='archivo_set', null=True, blank=True)

    def __str__(self):
        return self.NOMBRE
    
class Plantilla(models.Model):
    id = models.AutoField(primary_key=True)
    NOMBRE = models.CharField(max_length=255)
    NOMENCLATURA = models.CharField(max_length=255, null=False, blank=True)
    ACTIVO = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.NOMBRE


