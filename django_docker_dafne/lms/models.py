from django.db import models
from django.utils import timezone


class Usuario(models.Model):
    """Modelo de usuarios del sistema LMS"""
    ROL_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('instructor', 'Instructor'),
        ('admin', 'Administrador'),
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante')
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Curso(models.Model):
    """Modelo de cursos"""
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
        ('archivado', 'Archivado'),
    ]
    
    instructor = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    description = models.TextField()
    estado_publicacion = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    publicado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.publicado and not self.publicado_en:
            self.publicado_en = timezone.now()
            self.estado_publicacion = 'publicado'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


class Leccion(models.Model):
    """Modelo de lecciones para los cursos"""
    nombre_leccion = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, related_name='lecciones', on_delete=models.CASCADE)
    contenido = models.TextField()
    orden = models.PositiveIntegerField(default=0)
    n_modulos = models.PositiveIntegerField(default=1)
    duration = models.PositiveIntegerField(help_text="Duración en minutos", default=0)
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.nombre_leccion}"
    
    class Meta:
        verbose_name = "Lección"
        verbose_name_plural = "Lecciones"
        ordering = ['curso', 'orden']
        unique_together = ['curso', 'orden']


class Inscripcion(models.Model):
    """Modelo de inscripciones de usuarios a cursos"""
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    usuario = models.ForeignKey(Usuario, related_name='inscripciones', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, related_name='inscripciones', on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    inscrito_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.nombre} - {self.curso.titulo}"
    
    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ['usuario', 'curso']


class Comentario(models.Model):
    """Modelo para comentarios en cursos y lecciones"""
    usuario = models.ForeignKey(Usuario, related_name='comentarios', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, related_name='comentarios', on_delete=models.CASCADE)
    texto = models.TextField()
    referencia_leccion = models.ForeignKey(Leccion, related_name='comentarios', on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentario de {self.usuario.nombre} en {self.curso.titulo}"
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-creado_en']