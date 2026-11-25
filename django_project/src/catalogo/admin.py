# ==================================================================
# ARCHIVO  : catalogo/admin.py
# PARTE 1  : PRÁCTICA (Lucas): tienda en línea de la CAFETERÍA
# ROL      : DJANGO ADMIN de la app: Categoria y Producto.
# ==================================================================
from django.contrib import admin

from .models import Categoria, Producto

admin.site.register(Categoria)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo']
