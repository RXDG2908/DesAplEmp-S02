# ==================================================================
# ARCHIVO  : catalogo/api_views.py
# PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
# ROL      : CONTROLADORES de la API (en Django se llaman "views").
# ------------------------------------------------------------------
# LAB 14 - EJ 5: ProductoViewSet (ModelViewSet = CRUD completo) con
#                SearchFilter y search_fields; CategoriaViewSet de apoyo.
# ------------------------------------------------------------------
# USADO EN : ./api_urls.py  ·  SE PRUEBA: /api/productos/?search=caf
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 5 .... línea 29
# ==================================================================
from rest_framework import filters, viewsets

from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.order_by('nombre')
    serializer_class = CategoriaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    # Solo productos activos; select_related trae la categoría en la MISMA consulta.
    queryset = Producto.objects.filter(activo=True).select_related('categoria').order_by('nombre')
    serializer_class = ProductoSerializer
    # LAB 14 - EJ 5: ?search=texto busca en el nombre del producto y de su categoría.
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'categoria__nombre']
