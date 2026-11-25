# ==================================================================
# ARCHIVO  : servicios/serializers.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : MODEL <-> JSON de los rubros.
# ------------------------------------------------------------------
# LAB 14 - EJ 10: serializer del catálogo de rubros que usa el formulario de solicitudes.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 16
# ==================================================================
from rest_framework import serializers

from .models import Rubro


class RubroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubro
        fields = ['id', 'nombre', 'descripcion']
