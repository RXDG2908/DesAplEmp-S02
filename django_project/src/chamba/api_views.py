# ==================================================================
# ARCHIVO  : chamba/api_views.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : VISTA DE LA API -> CRUD COMPLETO de prestadores para el panel
#            de React: GET, POST, PUT, PATCH y DELETE.
# ------------------------------------------------------------------
# LAB 12 - EJ 9 : PrestadorViewSet (ModelViewSet) con BÚSQUEDA, FILTRO y ORDEN.
# LAB 12 - EJ 13: el panel envía ?search= y ?estado= y la API filtra aquí.
# ------------------------------------------------------------------
# SE PRUEBA: /api/chamba/prestadores/?search=ro&estado=Aprobado
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 12 - EJ 9 .... línea 23
#   LAB 12 - EJ 13 ... línea 33
# ==================================================================

from rest_framework import filters, viewsets

from .models import Prestador
from .serializers import PrestadorSerializer


class PrestadorViewSet(viewsets.ModelViewSet):
    serializer_class = PrestadorSerializer
    # BÚSQUEDA: ?search=texto busca en nombres y apellidos. ORDEN: ?ordering=tarifa.
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombres', 'apellidos']
    ordering_fields = ['tarifa', 'apellidos']

    def get_queryset(self):
        prestadores = Prestador.objects.all()
        # FILTRO POR CAMPO: /api/chamba/prestadores/?estado=Aprobado (vacío = todos).
        estado = self.request.query_params.get('estado')
        if estado:
            prestadores = prestadores.filter(estado=estado)
        return prestadores
