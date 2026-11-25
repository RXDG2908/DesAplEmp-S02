# ==================================================================
# ARCHIVO  : catalogo/models.py
# PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
# ROL      : la "M" de MVT -> TABLAS del catálogo: Categoria y Producto.
# ------------------------------------------------------------------
# LAB 13 - EJ 6: app creada vacía; aquí solo se DISEÑÓ.
# LAB 14 - EJ 2: modelos Categoria y Producto (precio DecimalField, stock
#                PositiveIntegerField, activo y FK a Categoria con PROTECT).
# LAB 14 - EJ 4: PROTECT impide borrar una categoría que tiene productos.
# ------------------------------------------------------------------
# USADO EN : ./serializers.py, ./api_views.py, ../pedidos/models.py, ../cargar_lab14.py
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 13 - EJ 6 .... línea 18
#   LAB 14 - EJ 2 .... línea 21
#   LAB 14 - EJ 4 .... línea 30
# ==================================================================
from django.db import models


class Categoria(models.Model):
    # SQL: nombre VARCHAR(80) NOT NULL
    nombre = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    # LAB 14 - EJ 4: PROTECT -> no se puede borrar una categoría con productos
    # (se perdería a qué categoría pertenece cada producto ya vendido).
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    nombre = models.CharField(max_length=120)
    # Dinero en DecimalField, nunca float: evita errores de redondeo.
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # PositiveIntegerField: la base de datos no acepta stock negativo.
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} (S/ {self.precio})'
