from django.contrib import admin

from .models import ARCHIVO, PERFIL, CARPETA, REPOSITORIO, UNIDAD_ORGANIZATIVA, Plantilla

class ARCHIVOAdmin(admin.ModelAdmin):
    list_display = ('NOMBRE','ARCHIVO','ID_CARPETA')
    search_fields = ('NOMBRE',)

class CARPETAAdmin(admin.ModelAdmin):
    list_display = ('NOMBRE','ID_PERFIL')
    search_fields = ('NOMBRE', 'ID_PERFIL')

class PERFILAdmin(admin.ModelAdmin):
    list_display = ('id','NOMBRES','APELLIDO_PATERNO','APELLIDO_MATERNO','ACTIVO','IMAGEN')
    search_fields = ('APELLIDO_PATERNO','id')

class REPOSITORIOAdmin(admin.ModelAdmin):
    search_fields = ('NOMBRE',)

class UOAdmin(admin.ModelAdmin):
    search_fields = ('NOMBRE',)

class PlantillaAdmin(admin.ModelAdmin):
    search_fields = ('NOMBRE',)

admin.site.register(ARCHIVO, ARCHIVOAdmin)
admin.site.register(CARPETA, CARPETAAdmin)
admin.site.register(PERFIL, PERFILAdmin)
admin.site.register(REPOSITORIO, REPOSITORIOAdmin)
admin.site.register(UNIDAD_ORGANIZATIVA, UOAdmin)
admin.site.register(Plantilla, PlantillaAdmin)