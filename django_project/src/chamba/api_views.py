# chamba/api_views.py
# CRUD de prestadores para el panel de React: GET, POST, PUT, PATCH y DELETE.

from rest_framework import filters, viewsets

from .models import Prestador
from .serializers import PrestadorSerializer


class PrestadorViewSet(viewsets.ModelViewSet):
    serializer_class = PrestadorSerializer
    # ?search=texto busca en nombres y apellidos; ?ordering=tarifa ordena.
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombres', 'apellidos']
    ordering_fields = ['tarifa', 'apellidos']

    def get_queryset(self):
        prestadores = Prestador.objects.all()
        # Filtro por campo: /api/chamba/prestadores/?estado=Aprobado
        estado = self.request.query_params.get('estado')
        if estado:
            prestadores = prestadores.filter(estado=estado)
        return prestadores
