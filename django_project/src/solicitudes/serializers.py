# ==================================================================
# ARCHIVO  : solicitudes/serializers.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : MODEL <-> JSON de la solicitud y REGLAS DE NEGOCIO antes de guardar.
# ------------------------------------------------------------------
# LAB 14 - EJ 11: validate_direccion (regla de un campo) y validate() con las reglas
#                 de la operación: prestador APROBADO, del MISMO RUBRO y SIN otro servicio
#                 en curso. El monto es de solo lectura: lo pone Django.
# ------------------------------------------------------------------
# USADO EN : ./api_views.py
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 11 ... líneas 46, 52
# ==================================================================
from rest_framework import serializers

from .models import SeguimientoSolicitud, Solicitud


class SeguimientoSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = SeguimientoSolicitud
        fields = ['estado', 'estado_nombre', 'fecha', 'nota']


class SolicitudSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.__str__', read_only=True)
    prestador_nombre = serializers.SerializerMethodField()
    rubro_nombre = serializers.CharField(source='rubro.nombre', read_only=True)
    estado_nombre = serializers.CharField(source='get_estado_display', read_only=True)
    seguimiento = SeguimientoSerializer(many=True, read_only=True)

    class Meta:
        model = Solicitud
        fields = ['id', 'cliente', 'cliente_nombre', 'prestador', 'prestador_nombre',
                  'rubro', 'rubro_nombre', 'direccion', 'descripcion', 'fecha',
                  'estado', 'estado_nombre', 'monto', 'seguimiento']
        # El estado cambia con la acción /avanzar/ y el monto lo calcula Django.
        read_only_fields = ['fecha', 'estado', 'monto']

    def get_prestador_nombre(self, obj):
        return f'{obj.prestador.nombres} {obj.prestador.apellidos}'

    # LAB 14 - EJ 11: REGLA DE UN CAMPO -> el prestador necesita una dirección clara.
    def validate_direccion(self, value):
        if len(value.strip()) < 8:
            raise serializers.ValidationError('La dirección debe tener al menos 8 caracteres.')
        return value.strip()

    # LAB 14 - EJ 11: REGLAS DE LA OPERACIÓN (usan varios campos a la vez).
    def validate(self, datos):
        prestador = datos.get('prestador') or getattr(self.instance, 'prestador', None)
        rubro = datos.get('rubro') or getattr(self.instance, 'rubro', None)
        if prestador.estado != 'Aprobado':
            raise serializers.ValidationError({'prestador': 'Solo un prestador Aprobado puede recibir solicitudes.'})
        if prestador.rubro != rubro.nombre:
            raise serializers.ValidationError({'rubro': f'{prestador.nombres} no atiende {rubro.nombre}.'})
        ocupado = Solicitud.objects.filter(prestador=prestador, estado__in=Solicitud.EN_CURSO)
        if self.instance:
            ocupado = ocupado.exclude(pk=self.instance.pk)
        if ocupado.exists():
            raise serializers.ValidationError({'prestador': 'El prestador ya tiene un servicio en curso.'})
        return datos
