from django.contrib import admin

# Register your models here.
from .models import Usuario, Curso, Leccion, Inscripcion, Comentario

admin.site.register(Usuario)
admin.site.register(Curso)
admin.site.register(Leccion)
admin.site.register(Inscripcion)
admin.site.register(Comentario)
