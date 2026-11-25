# ==================================================================
# ARCHIVO  : catalogo/admin.py
# PARTE 1  : PRÁCTICA (Lucas): tienda en línea de la CAFETERÍA
# ROL      : DJANGO ADMIN de la app: Categoria y Producto.
# ------------------------------------------------------------------
# LAB 14 - EJ 3: registra Categoria y Producto para revisar en /admin/ los datos del shell.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 3 .... línea 15
# ==================================================================
from django.contrib import admin

from .models import Categoria, Producto

admin.site.register(Categoria)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo']
