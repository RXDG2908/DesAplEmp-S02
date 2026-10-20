from datetime import date

from rest_framework import serializers

from .models import Categoria, Libro, Prestamo, Socio


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'isbn', 'anio_publicacion',
                  'copias', 'categoria']

    def validate_anio_publicacion(self, value):
        if value < 1450 or value > date.today().year:
            raise serializers.ValidationError(
                'El año de publicación debe estar entre 1450 y el año actual.')
        return value


class SocioResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = ['id', 'nombre', 'dni']


class LibroResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor']


class PrestamoSerializer(serializers.ModelSerializer):
    socio = SocioResumenSerializer(read_only=True)
    libro = LibroResumenSerializer(read_only=True)

    class Meta:
        model = Prestamo
        fields = ['id', 'socio', 'libro', 'fecha_prestamo',
                  'fecha_devolucion_prevista', 'fecha_devolucion_real',
                  'estado', 'multa']