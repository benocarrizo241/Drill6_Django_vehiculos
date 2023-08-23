from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import VehiculoForm, RegistroUsuarioForm

from django.http import HttpResponse, HttpResponseRedirect
from tokenize import PseudoExtras
from django.contrib.auth import login, authenticate, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import VehiculoModel

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.views import View

from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.


class IndexPageView(PermissionRequiredMixin,LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    permission_required= 'vehiculo.delete_vehiculomodel '
    template_name = 'index.html'

    #def get(request):
     #   return render(request, 'index.html', {})


def indexView(request):
    has_add_permission = request.user.has_perm('vehiculo.add_vehiculomodel')
    context = {'has_add_permission': has_add_permission}
    #template_name = 'index.html'
    return render(request, 'index.html', context)

    #permiso con logeo, hay una linea mas en setting.py (LOGIN_URL = 'login') y from django.contrib.auth.decorators import login_required
@login_required
@permission_required('vehiculo.add_vehiculomodel', raise_exception=True, login_url='/add')
def addVehiculo(request):
    has_add_permission = request.user.has_perm('vehiculo.add_vehiculomodel')
    form = VehiculoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form= VehiculoForm()
        messages.success(request, 'Los datos se han procesado exitosamente')

    return render(request, "addform.html", {'form': form, 'has_add_permission': has_add_permission})

def registro_view(request):
        if request.method == "POST":
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                # Obtener el contenido y permiso para visualizar el catálogo
                try:
                    content_type = ContentType.objects.get_for_model(VehiculoModel)
                    
                    visualizar_catalogo = Permission.objects.get(codename='visualizar_catalogo', content_type=content_type)
                    user = form.save()
                except (ContentType.DoesNotExist, Permission.DoesNotExist):
                    # Manejar excepciones si no se encuentra el modelo o el permiso
                    messages.error(request, "Error en el registro. Por favor, contacte al administrador.")
                    return HttpResponseRedirect('/')

                user.user_permissions.add(visualizar_catalogo)
                login(request, user)
                messages.success(request, "Usuario registrado exitosamente.")
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "Registro inválido. Algunos datos incorrectos. Verifique.")
        #else:
        form = RegistroUsuarioForm()
        
        context = {"register_form": form}
        return render(request, "registro.html", context)

def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"Iniciaste sesión como: {username}.")
                
                    return HttpResponseRedirect("/")
                else:
                    messages.error(request, "Username o password inválido!!")
            else:
                messages.error(request, "Username o password inválido!!")
        form = AuthenticationForm()
        context= {"login_form": form}        
        return render(request, "login.html", context) 

@login_required
def listar_vehiculo(request):
        vehiculos = VehiculoModel.objects.all()
        has_add_permission = request.user.has_perm('vehiculo.add_vehiculomodel')
        context = {'lista_vehiculos': vehiculos, 'has_add_permission': has_add_permission }
        return render(request, 'listar.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "Se ha cerrado la sesion satisfactoriamente.")
    return HttpResponseRedirect('/')
