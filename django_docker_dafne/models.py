from django.db import models
from django.contrib.auth.models import User

class Cursos(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    maestro_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cursos')
    creado_en = models.DateTimeField(auto_now_add=True)
    publicado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    rol = models.CharField(max_length=50, default='alumno')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}".strip()


class Inscripciones(models.Model):
    usuario_id = models.IntegerField()
    curso_id = models.IntegerField()
    estado = models.CharField(max_length=20, default='activa')  
    inscrito_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inscripción usuario {self.usuario_id} → curso {self.curso_id}"


class Lecciones(models.Model):
    nombre_leccion = models.CharField(max_length=150)
    curso_id = models.IntegerField()
    contenido = models.TextField()
    orden = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.orden}. {self.nombre_leccion}"


class Comentarios(models.Model):
    usuario_id = models.IntegerField()
    curso_id = models.IntegerField()
    texto = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de usuario {self.usuario_id} en curso {self.curso_id}"
