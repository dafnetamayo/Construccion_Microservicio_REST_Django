from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'lecciones', views.LeccionViewSet)
router.register(r'inscripciones', views.InscripcionViewSet)
router.register(r'comentarios', views.ComentarioViewSet)


# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('usuario-view/', views.usuario_view, name='usuario-view'),
    path('curso-view/', views.curso_view, name='curso-view'),
    path('accounts/google/login/callback/', views.google_callback, name='google_callback')
]
