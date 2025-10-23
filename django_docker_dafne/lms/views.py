from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from .forms import RegistroForm, LoginForm

from .models import Usuario, Curso, Leccion, Inscripcion, Comentario
from .serializers import (
    UsuarioSerializer, CursoSerializer, LeccionSerializer,
    InscripcionSerializer, ComentarioSerializer
)


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Crear un usuario en nuestro modelo personalizado
            usuario = Usuario(
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                email=form.cleaned_data['email'],
                rol='estudiante'
            )
            usuario.save()
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def iniciar_sesion(request):
    """Vista para iniciar sesión con credenciales normales o con Google OAuth"""
    google_provider_enabled = True
    try:
        from allauth.socialaccount.models import SocialApp
        google_provider_enabled = SocialApp.objects.filter(
            provider='google').exists()
    except Exception as e:
        # allauth may not be available or DB may not have SocialApp entries.
        print("Google provider not enabled:", str(e))
        google_provider_enabled = False

    # Si el usuario ya está autenticado con Django, verificar si tiene una cuenta social
    if request.user.is_authenticated:
        try:
            # Verificar si el usuario tiene una cuenta social de Google
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            
            # Verificar si ya existe un Usuario con este email
            try:
                usuario = Usuario.objects.get(email=request.user.email)
            except Usuario.DoesNotExist:
                # Crear un nuevo Usuario basado en la cuenta de Google
                usuario = Usuario.objects.create(
                    nombre=request.user.first_name or "Usuario",
                    apellido=request.user.last_name or "Google",
                    email=request.user.email,
                    rol='estudiante'  # Rol por defecto
                )
            # Guardar el ID del usuario en la sesión
            request.session['usuario_id'] = usuario.id
            next_url = request.GET.get('next', 'perfil')
            return redirect(next_url)
        except SocialAccount.DoesNotExist:
            # El usuario está autenticado pero no con Google
            pass

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                usuario = Usuario.objects.get(email=email)
                request.session['usuario_id'] = usuario.id
                next_url = request.GET.get('next', 'perfil')
                return redirect(next_url)
            except Usuario.DoesNotExist:
                messages.error(request, 'Credenciales incorrectas')
                return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {
        'form': form,
        'google_provider_enabled': google_provider_enabled
    })


def perfil(request):
    # Verificamos si el usuario está autenticado en nuestro sistema
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        # Si no está autenticado, redirigimos a login con next parameter
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        
        # Obtenemos los cursos disponibles
        cursos_disponibles = Curso.objects.filter(publicado=True).order_by('-creado_en')[:10]
        
        # Obtenemos los cursos en los que el usuario está inscrito
        inscripciones = Inscripcion.objects.filter(usuario=usuario)
        cursos_inscritos = [inscripcion.curso for inscripcion in inscripciones]
        
        context = {
            'usuario': usuario,
            'cursos_disponibles': cursos_disponibles,
            'cursos_inscritos': cursos_inscritos
        }
        
        return render(request, 'usuarios/perfil.html', context)
    except Usuario.DoesNotExist:
        # Si el usuario no existe, eliminamos la sesión y redirigimos a login
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        return redirect('login')


def cerrar_sesion(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    # También cerrar la sesión de Django si está autenticado
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def google_callback(request):
    """
    Vista para manejar el callback de Google OAuth
    Esta función se llama automáticamente por django-allauth después de la autenticación con Google
    """
    # Si el usuario está autenticado con Django después del callback de Google
    if request.user.is_authenticated:
        try:
            # Verificar si el usuario tiene una cuenta social de Google
            social_account = SocialAccount.objects.get(user=request.user, provider='google')
            
            # Obtener datos extra del perfil de Google
            extra_data = social_account.extra_data
            
            # Verificar si ya existe un Usuario con este email
            try:
                usuario = Usuario.objects.get(email=request.user.email)
            except Usuario.DoesNotExist:
                # Crear un nuevo Usuario basado en la cuenta de Google
                usuario = Usuario.objects.create(
                    nombre=extra_data.get('given_name', request.user.first_name) or "Usuario",
                    apellido=extra_data.get('family_name', request.user.last_name) or "Google",
                    email=request.user.email,
                    rol='estudiante'  # Rol por defecto
                )
            # Guardar el ID del usuario en la sesión
            request.session['usuario_id'] = usuario.id
            messages.success(request, f'Bienvenido, {usuario.nombre}!')
        except SocialAccount.DoesNotExist:
            messages.error(request, 'Error al procesar la cuenta de Google')
    
    next_url = request.GET.get('next', 'perfil')
    return redirect(next_url)


def index(request):
    # Show up to 20 published courses on the home page
    cursos = Curso.objects.filter(
        publicado=True).order_by('-creado_en')[:20]
    return render(request, 'index.html', {'cursos': cursos})

def usuario_view(request):
    # Todos los cursos a los que un usuario esta inscrito
    try:
        inscripciones = Inscripcion.objects.filter(usuario=request.user)
        cursos = [inscripcion.curso for inscripcion in inscripciones]
        return render(request, 'usuarios/usuario_view.html', {'cursos': cursos})
    except Inscripcion.DoesNotExist:
        return render(request, 'usuarios/usuario_view.html', {'cursos': []})

def curso_view(request):
    # Todos los datos de un curso
    curso = Curso.objects.get(id=request.GET.get('curso_id'))
    return render(request, 'cursos/curso_view.html', {'curso': curso}) # Donde curso es un objeto con los atributos del modelo


class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Usuario"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rol']
    search_fields = ['nombre', 'apellido', 'email']
    ordering_fields = ['nombre', 'apellido', 'creado_en']
    ordering = ['apellido', 'nombre']


class CursoViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Curso"""
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado_publicacion', 'publicado']
    search_fields = ['titulo', 'description']
    ordering_fields = ['titulo', 'creado_en']
    ordering = ['-creado_en']


class LeccionViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Leccion"""
    queryset = Leccion.objects.all()
    serializer_class = LeccionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['curso']
    search_fields = ['nombre_leccion', 'contenido']
    ordering_fields = ['orden', 'nombre_leccion']
    ordering = ['curso', 'orden']


class InscripcionViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Inscripcion"""
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'curso', 'usuario']
    search_fields = ['curso__titulo']
    ordering_fields = ['inscrito_en']
    ordering = ['-inscrito_en']

    def perform_create(self, serializer):
        # En un sistema real, obtendríamos el usuario actual
        usuario_id = self.request.session.get('usuario_id')
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                serializer.save(usuario=usuario)
            except Usuario.DoesNotExist:
                pass


class ComentarioViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Comentario"""
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['curso', 'referencia_leccion']
    search_fields = ['texto']
    ordering_fields = ['creado_en']
    ordering = ['-creado_en']

    def perform_create(self, serializer):
        # En un sistema real, obtendríamos el usuario actual
        usuario_id = self.request.session.get('usuario_id')
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                serializer.save(usuario=usuario)
            except Usuario.DoesNotExist:
                pass