# ==================================================================
# GUIA: ARCHIVO  biblioteca/api_views.py  (vistas de la API de la biblioteca)
# LAB     : 08 Parte 2
# EJERCICIO: ViewSets de Categoria y Libro (search/ordering), Prestamo solo lectura con ?estado=
#           y @action con_multa (reutiliza PrestamoQuerySet.con_multa del Lab 07 P2).
# SE PRUEBA: /api/biblioteca/libros/?search=cosmos - /api/biblioteca/prestamos/con_multa/
# DOCS    : ../../README.md (seccion Lab 8 Parte 2)
# ==================================================================
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Categoria, Libro, Prestamo
from .serializers import (CategoriaSerializer, LibroSerializer,
                          PrestamoSerializer)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.order_by('nombre')
    serializer_class = CategoriaSerializer


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.order_by('titulo')
    serializer_class = LibroSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'autor', 'isbn']
    ordering_fields = ['titulo', 'anio_publicacion', 'copias']


class PrestamoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PrestamoSerializer

    def get_queryset(self):
        prestamos = Prestamo.objects.select_related('socio', 'libro')
        estado = self.request.query_params.get('estado')
        if estado:
            prestamos = prestamos.con_estado(estado)
        return prestamos

    @action(detail=False)
    def con_multa(self, request):
        prestamos = self.get_queryset().con_multa()
        serializer = self.get_serializer(prestamos, many=True)
        return Response(serializer.data)