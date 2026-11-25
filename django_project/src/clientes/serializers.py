# ==================================================================
# ARCHIVO  : clientes/serializers.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : MODEL <-> JSON de los clientes.
# ------------------------------------------------------------------
# LAB 14 - EJ 10: serializer de Cliente para el panel.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 16
# ==================================================================
from rest_framework import serializers

from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombres', 'apellidos', 'telefono', 'email']
