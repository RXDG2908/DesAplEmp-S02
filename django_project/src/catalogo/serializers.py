# ==================================================================
# ARCHIVO  : catalogo/serializers.py
# PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
# ROL      : MODEL <-> JSON del catálogo y VALIDACIÓN de lo que llega.
# ------------------------------------------------------------------
# LAB 14 - EJ 5: ProductoSerializer con la regla validate_precio (precio > 0)
#                y el nombre de la categoría para mostrarlo en React.
# ------------------------------------------------------------------
# USADO EN : ./api_views.py
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 5 .... línea 33
# ==================================================================
from rest_framework import serializers

from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class ProductoSerializer(serializers.ModelSerializer):
    # Solo lectura: React muestra el nombre sin pedir otra vez la categoría.
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'activo', 'categoria', 'categoria_nombre']

    # LAB 14 - EJ 5: REGLA DE NEGOCIO -> un producto no puede costar cero ni menos.
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor que cero.')
        return value
