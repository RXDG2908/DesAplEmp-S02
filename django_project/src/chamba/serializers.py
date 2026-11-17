# ==================================================================
# ARCHIVO  : chamba/serializers.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : MODEL <-> JSON. CONVIERTE los prestadores a JSON y VALIDA
#            lo que llega desde el panel de React.
# ------------------------------------------------------------------
# LAB 12 - EJ 9 : PrestadorSerializer con la REGLA validate_tarifa.
# LAB 12 - EJ 11: esa regla produce el ERROR 400 que el formulario MUESTRA.
# ------------------------------------------------------------------
# USADO EN : ./api_views.py
# ==================================================================

from rest_framework import serializers

from .models import Prestador


class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestador
        fields = ['id', 'nombres', 'apellidos', 'rubro', 'tarifa', 'estado']

    # LAB 12 - EJ 9: REGLA DE NEGOCIO -> la TARIFA por visita debe ser MAYOR QUE CERO.
    # Si no se cumple, la API responde 400 BAD REQUEST con este mensaje.
    def validate_tarifa(self, value):
        if value <= 0:
            raise serializers.ValidationError('La tarifa debe ser mayor que cero.')
        return value
