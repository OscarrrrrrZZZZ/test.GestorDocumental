from django.shortcuts import render, redirect, get_object_or_404
from .models import Folder, File, REPOSITORIO,PERFIL,CARPETA,UNIDAD_ORGANIZATIVA, ARCHIVO, Plantilla, User
from .forms import FolderForm, FileForm, ArchivoForm, PlantillaForm
from django.http import JsonResponse
from django.shortcuts import render
from datetime import date
from django.http import JsonResponse
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .models import PERFIL
from .forms import ArchivoForm
from django.db.models import Count
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    plantillas = Plantilla.objects.all()
    perfiles = PERFIL.objects.all()
    return render(request, 'buscador/home.html', {'plantillas': plantillas, 'perfiles': perfiles})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'buscador/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Clear any existing failed attempts for this user
                cache.delete(f'login_attempts_{username}')
                # Redirect to a success page (e.g., home)
                return redirect('buscar_archivos')  # Adjust 'buscar_archivos' to your actual URL name for success
            else:
                # Increment failed attempts counter for the user
                attempts = cache.get(f'login_attempts_{username}', 0)
                attempts += 1
                cache.set(f'login_attempts_{username}', attempts, timeout=settings.LOGIN_ATTEMPT_TIMEOUT)

                form.add_error(None, "Usuario o contraseña incorrectos.")
        else:
            form.add_error(None, "Usuario o contraseña incorrectos.")
            messages.add_message(request, 50, "Usuario o contraseña incorrectos.")
        
        # Retrieve the current number of attempts if username is defined
        username = form.cleaned_data.get('username')  # Ensure username is defined here
        if username:
            attempts = cache.get(f'login_attempts_{username}', 0)
            if attempts >= settings.MAX_LOGIN_ATTEMPTS:
                form.add_error(None, "Tu cuenta ha sido bloqueada debido a múltiples intentos fallidos.")
                # Optionally, you can disable the form submission here to prevent further attempts

        # If authentication fails or form is invalid, re-render the login page with errors
        return render(request, 'buscador/login.html', {'form': form})

def buscar_funcionarios(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        query = request.GET.get('query', '')

        # Concatenar los campos para la búsqueda por nombre completo
        funcionarios = PERFIL.objects.annotate(
            nombre_completo=Concat('NOMBRES', Value(' '), 'APELLIDO_PATERNO', Value(' '), 'APELLIDO_MATERNO')
        ).filter(
            Q(NOMBRES__icontains=query) |
            Q(APELLIDO_PATERNO__icontains=query) |
            Q(APELLIDO_MATERNO__icontains=query) |
            Q(id__icontains=query) |
            Q(nombre_completo__icontains=query)
        )

        results = []
        for funcionario in funcionarios:
            results.append({
                'id': funcionario.id,
                'imagen': funcionario.IMAGEN.url if funcionario.IMAGEN else '',
                'nombres': funcionario.NOMBRES,
                'apellido_paterno': funcionario.APELLIDO_PATERNO,
                'apellido_materno': funcionario.APELLIDO_MATERNO,
            })
        return JsonResponse(results, safe=False)
    return JsonResponse({"error": "Invalid request"}, status=400)


def unidades_organizativas(request):
    unidades = UNIDAD_ORGANIZATIVA.objects.all().values('id', 'NOMBRE')
    return JsonResponse(list(unidades), safe=False)

def detalle_perfil(request, perfil_id):
    # Obtener el perfil según el perfil_id
    perfil = get_object_or_404(PERFIL, id=perfil_id)
    
    # Obtener las carpetas asociadas a ese perfil y anotar el conteo de archivos
    carpetas = CARPETA.objects.filter(ID_PERFIL=perfil).annotate(archivo_count=Count('archivo_set'))
    
    # Renderizar el template para mostrar las carpetas asociadas al perfil
    return render(request, 'folders/visualizacioncarpetas.html', {'perfil': perfil, 'carpetas': carpetas })

def detalle_carpeta(request, carpeta_id):
    carpeta = get_object_or_404(CARPETA, id=carpeta_id)
    archivos = ARCHIVO.objects.filter(ID_CARPETA=carpeta)
    perfil = carpeta.ID_PERFIL
    archivo_count = archivos.count()
    return render(request, 'subfolders/detalle_carpeta.html', {'carpeta': carpeta, 'archivos': archivos, 'perfil': perfil})


def cargar_archivo(request):
    if request.method == 'POST':
        form = ArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Archivo Guardado Con Éxito')
            return redirect('buscar_archivos')  # Redirige a la página de inicio u otra página después de guardar
        else:
            messages.error(request, 'Error al cargar archivo.')
            
    else:
        form = ArchivoForm()
    perfiles = PERFIL.objects.all()
    plantillas = Plantilla.objects.all()
    return render(request, 'cargar_archivo.html', {'form': form, 'perfiles': perfiles, 'plantillas':plantillas})

def buscar_perfil(request):
    query = request.GET.get('q', '')
    if query:
        # Dividir el query en palabras
        query_words = query.split()
        
        # Crear un filtro inicial vacío
        q_objects = Q()
        
        # Añadir un filtro para cada palabra en el query
        for word in query_words:
            q_objects &= (Q(NOMBRES__icontains=word) | 
                          Q(APELLIDO_PATERNO__icontains=word) | 
                          Q(APELLIDO_MATERNO__icontains=word))
        
        # Filtrar los perfiles utilizando el filtro acumulado
        perfiles = PERFIL.objects.filter(q_objects)
    else:
        perfiles = PERFIL.objects.none()

    perfiles = list(perfiles.values('id', 'NOMBRES', 'APELLIDO_PATERNO', 'APELLIDO_MATERNO'))
    return JsonResponse({'perfiles': perfiles})

def cargar_carpetas(request, perfil_id):
    carpetas = CARPETA.objects.filter(ID_PERFIL_id=perfil_id)
    carpetas = list(carpetas.values('id', 'NOMBRE'))
    return JsonResponse({'carpetas': carpetas})

def listar_carpetas(request):
    carpetas = CARPETA.objects.all()
    return render(request, 'folders/visualizacioncarpetas.html', {'carpetas': carpetas})

def listar_resoluciones(request):
    archivos = ARCHIVO.objects.all()
    return render(request, 'operation/archivosCargados.html', {'archivos': archivos})

def listar_resoluciones_masivas(request):
    archivos = ARCHIVO.objects.filter(MASIVA=True)
    return render(request, 'operation/resMasivasIPS.html', {'archivos': archivos})


def guardar_perfil(request):
    if request.method == 'POST':
        try:
            perfil_id = request.POST.get('perfil_id')
            nombres = request.POST.get('nombres')
            apellido_paterno = request.POST.get('apellido_paterno')
            apellido_materno = request.POST.get('apellido_materno')
            activo = request.POST.get('activo') == 'true'
            imagen = request.FILES.get('imagen')
            fecha_contratacion = request.POST.get('fecha_contratacion')
            uo_id = request.POST.get('uo_id')

            # Convertir fecha_contratacion a objeto Date
            fecha_contratacion = date.fromisoformat(fecha_contratacion)

            # Crear el perfil
            nuevo_perfil = PERFIL(
                id=perfil_id,
                NOMBRES=nombres,
                APELLIDO_PATERNO=apellido_paterno,
                APELLIDO_MATERNO=apellido_materno,
                ACTIVO=activo,
                IMAGEN=imagen,
                FECHA_CONTRATACION=fecha_contratacion,
                UO_ID_id=uo_id
            )
            nuevo_perfil.save()

            # Crear las carpetas asociadas al perfil
            nombres_carpetas = [
                'VIDA FUNCIONARIA',
                'REMUNERACIONES',
                'CALIFICACIONES',
                'ESTUDIOS CAPACITACION',
                'ANTECEDENTES VARIOS'
            ]

            for nombre_carpeta in nombres_carpetas:
                nueva_carpeta = CARPETA(
                    NOMBRE=nombre_carpeta,
                    ID_PERFIL=nuevo_perfil
                )
                nueva_carpeta.save()

            return JsonResponse({'message': 'Perfil creado correctamente.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)


def funcionariosActivosIPS(request):
    activos = PERFIL.objects.all()
    
    return render(request, 'operation/funcionariosActivosIPS.html', {'activos': activos, 'user': request.user})

def funcionariosInactivosIPS(request):
    inactivos = PERFIL.objects.filter(ACTIVO = False)
    return render(request, 'operation/funcionariosInactivosIPS.html', {'inactivos': inactivos})


def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    subfolders = folder.subfolders.all()
    files = folder.files.all()
    return render(request, 'buscador/folder_detail.html', {
        'folder': folder,
        'subfolders': subfolders,
        'files': files
    })

def create_folder(request, parent_id=None):
    parent_folder = None
    if parent_id:
        parent_folder = get_object_or_404(Folder, id=parent_id)
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            new_folder = form.save()
            return redirect('folder_detail', folder_id=new_folder.id)
    else:
        form = FolderForm(initial={'parent': parent_folder})
    return render(request, 'buscador/folder_form.html', {'form': form})

def upload_file(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save()
            return redirect('folder_detail', folder_id=folder.id)
    else:
        form = FileForm(initial={'folder': folder})
        
    return render(request, 'buscador/file_form.html', {'form': form})

def obtener_plantillas(request):
    plantillas = Plantilla.objects.all().values('id', 'NOMBRE', 'NOMENCLATURA')
    return JsonResponse(list(plantillas), safe=False)

def admin_plantillas(request):
    plantillas = Plantilla.objects.all()
    return render(request, 'administration/admin-plantillas.html', {'plantillas':plantillas})

def admin_usuarios(request):
    usuario = User.objects.all()
    return render(request, 'administration/admin-user.html', {'usuario': usuario})

def panel_administracion(request):
    return render(request, 'administration/panel-administracion.html')

def crear_plantilla(request):
    if request.method == 'POST':
        form = PlantillaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plantilla creada con éxito.')
            return redirect('administrar_plantillas')
        else:
            messages.error(request, 'Error al crear la plantilla.')
    else:
        form = PlantillaForm()

    return render(request, 'crear_plantilla.html', {'form': form})

def editar_plantilla(request, id):
    plantilla = get_object_or_404(Plantilla, id=id)

    if request.method == 'POST':
        form = PlantillaForm(request.POST, instance=plantilla)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plantilla actualizada con éxito.')
            return JsonResponse({'success': True})
        else:
            messages.error(request, 'Error al actualizar la plantilla.')
            return JsonResponse({'success': False, 'errors': form.errors})

    form = PlantillaForm(instance=plantilla)
    return render(request, 'editar_plantilla.html', {'form': form})

def eliminar_plantilla(request, id):
    plantilla = get_object_or_404(Plantilla, id=id)
    if request.method == 'POST':
        plantilla.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
