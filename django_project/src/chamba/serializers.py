# chamba/serializers.py
# Convierte los prestadores a JSON y valida lo que llega del panel.

from rest_framework import serializers

from .models import Prestador


class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestador
        fields = ['id', 'nombres', 'apellidos', 'rubro', 'tarifa', 'estado']

    # Regla de negocio: la tarifa por visita debe ser mayor que cero.
    def validate_tarifa(self, value):
        if value <= 0:
            raise serializers.ValidationError('La tarifa debe ser mayor que cero.')
        return value
