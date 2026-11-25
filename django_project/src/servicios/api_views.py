# ==================================================================
# ARCHIVO  : servicios/api_views.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : CONTROLADOR de los rubros (solo lectura).
# ------------------------------------------------------------------
# LAB 14 - EJ 10: los rubros se consultan; se crean desde el Django Admin.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 17
# ==================================================================
from rest_framework import viewsets

from .models import Rubro
from .serializers import RubroSerializer


class RubroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rubro.objects.all()
    serializer_class = RubroSerializer
