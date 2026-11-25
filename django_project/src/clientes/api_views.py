# ==================================================================
# ARCHIVO  : clientes/api_views.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : CONTROLADOR de los clientes (CRUD con búsqueda).
# ------------------------------------------------------------------
# LAB 14 - EJ 10: ClienteViewSet con ?search= por nombres, apellidos o email.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 17
# ==================================================================
from rest_framework import filters, viewsets

from .models import Cliente
from .serializers import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombres', 'apellidos', 'email']
