from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('folder/<int:folder_id>/', login_required(views.folder_detail), name='folder_detail'),
    path('folder/create/', login_required(views.create_folder), name='create_folder'),
    path('folder/<int:folder_id>/create/', login_required(views.create_folder), name='create_subfolder'),
    path('folder/<int:folder_id>/upload/', login_required(views.upload_file), name='upload_file'),
    path('funcionariosActivosIPS', login_required(views.funcionariosActivosIPS), name='funcionariosActivosIPS'),
    path('funcionariosInactivosIPS', login_required(views.funcionariosInactivosIPS), name='funcionariosInactivosIPS'),
    path('resoluciones_masivas', login_required(views.listar_resoluciones_masivas), name='resoluciones_masivas'),
    path('buscar_funcionarios/', login_required(views.buscar_funcionarios), name='buscar_funcionarios'),
    path('detalle_perfil/<int:perfil_id>/', login_required(views.detalle_perfil), name='detalle_perfil'),
    path('detalle_perfil/<int:perfil_id>/', login_required(views.detalle_perfil), name='detalle_perfil'),
    path('api/unidades_organizativas/', login_required(views.unidades_organizativas), name='api_unidades_organizativas'),
    path('guardar_perfil/', login_required(views.guardar_perfil), name='guardar_perfil'),
    path('cargar_archivo/', login_required(views.cargar_archivo), name='cargar_archivo'),
    path('buscar_perfil/', login_required(views.buscar_perfil), name='buscar_perfil'),
    path('cargar_carpetas/<int:perfil_id>/', login_required(views.cargar_carpetas), name='cargar_carpetas'),
    path('carpetas/', login_required(views.listar_carpetas), name='listar_carpetas'),
    path('carpeta/<int:carpeta_id>/', login_required(views.detalle_carpeta), name='detalle_carpeta'),
    path('buscar_archivos', login_required(views.listar_resoluciones), name='buscar_archivos'),
    path('', login_required(views.listar_resoluciones), name='buscar_archivos'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('home/',login_required(views.home), name='home'),
    path('api/obtener-plantillas/', login_required(views.obtener_plantillas), name='api_obtener_plantillas'),
    path('admin-plantillas/', login_required(views.admin_plantillas), name='administrar_plantillas'),
    path('admin-usuarios/', login_required(views.admin_usuarios), name='admin_usuarios'),
    path('panel-administracion/', login_required(views.panel_administracion), name='panel_administracion'),
]