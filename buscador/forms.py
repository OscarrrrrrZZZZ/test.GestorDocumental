from django import forms
from .models import Folder, File, REPOSITORIO, PERFIL, CARPETA, ARCHIVO, UNIDAD_ORGANIZATIVA, Plantilla
class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'parent']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'folder']

class REPOSITORIOForms(forms.ModelForm):
    class Meta:
        model = REPOSITORIO
        fields = ['NOMBRE']

class PERFILForms(forms.ModelForm):
    class Meta:
        model = PERFIL
        fields = ['NOMBRES', 'APELLIDO_PATERNO', 'APELLIDO_MATERNO','IMAGEN','ACTIVO']

class CARPETASForms(forms.ModelForm):
    class Meta:
        model = CARPETA
        fields = ['NOMBRE', 'ID_PERFIL']

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = ARCHIVO
        fields = ['NOMBRE', 'ARCHIVO', 'MASIVA', 'ID_CARPETA']  

class PlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = ['NOMBRE','NOMENCLATURA']  

