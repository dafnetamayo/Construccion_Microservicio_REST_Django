from rest_framework import serializers
from .models import Usuario, Curso, Leccion, Inscripcion, Comentario


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Usuario"""
    
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'email', 'rol', 'creado_en']
        read_only_fields = ['id', 'creado_en']


class CursoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Curso"""
    
    class Meta:
        model = Curso
        fields = [
            'id', 'instructor', 'titulo', 'description',
            'estado_publicacion', 'publicado_en', 'creado_en', 'publicado'
        ]
        read_only_fields = ['id', 'creado_en', 'publicado_en']


class LeccionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Leccion"""
    
    class Meta:
        model = Leccion
        fields = [
            'id', 'nombre_leccion', 'curso', 'contenido',
            'orden', 'n_modulos', 'duration'
        ]
        read_only_fields = ['id']


class InscripcionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Inscripcion"""
    
    class Meta:
        model = Inscripcion
        fields = ['id', 'usuario', 'curso', 'estado', 'inscrito_en']
        read_only_fields = ['id', 'inscrito_en']


class ComentarioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Comentario"""
    
    class Meta:
        model = Comentario
        fields = ['id', 'usuario', 'curso', 'texto', 'referencia_leccion', 'creado_en']
        read_only_fields = ['id', 'creado_en']
