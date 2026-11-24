# ==================================================================
# ARCHIVO  : vet/serializers.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : MODEL <-> JSON. Es el "FORM" de la API (Django REST Framework):
#            SERIALIZA instancias a JSON y VALIDA el JSON que llega
#            (DESERIALIZA) antes de guardarlo.
# ------------------------------------------------------------------
# LAB 8 - EJ 2: InsumoSerializer -> MODELSERIALIZER del recurso SIMPLE.
# LAB 8 - EJ 3: validate_stock -> REGLA DE NEGOCIO (stock inicial >= 1).
# LAB 8 - EJ 7: CitaSerializer -> recurso CON RELACIONES ANIDADAS (solo lectura).
# ------------------------------------------------------------------
# USADO EN : ./api_views.py
# SE PRUEBA: /api/insumos/  ·  /api/citas/
# DOCS     : ../../../docs/guiones/GUION-Lab08-Parte1.md
#            ../../../docs/exposiciones/EXPOSICION_Lab08_Parte1.md
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 8 - EJ 2 ..... línea 28
#   LAB 8 - EJ 3 ..... líneas 28, 34
#   LAB 8 - EJ 7 ..... líneas 45, 60, 71, 73, 75
# ==================================================================

from rest_framework import serializers

from .models import Cita, ConsumoInsumo, FichaClinica, Insumo, Veterinario


# --- LAB 8 - EJ 2 y 3: recurso SIMPLE con una REGLA DE NEGOCIO ---------
class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ['id', 'nombre', 'unidad', 'stock']

    # LAB 8 - EJ 3: validate_<campo> -> DRF lo llama SOLO dentro de is_valid().
    # REGLA DE NEGOCIO: un insumo se da de alta con AL MENOS 1 UNIDAD en stock;
    # registrar un insumo sin existencias no tiene sentido en el almacén.
    # Si falla, la API responde 400 BAD REQUEST con este mensaje.
    def validate_stock(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'El stock inicial debe ser de al menos 1 unidad.')
        return value


# --- LAB 8 - EJ 7: recurso CON RELACIONES (SOLO LECTURA, ANIDADO) ------
# Cada serializer pequeño se INCRUSTA dentro de CitaSerializer.
class VeterinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinario
        fields = ['id', 'nombre', 'colegiatura', 'especialidad']


class FichaClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaClinica
        fields = ['peso_kg', 'diagnostico', 'tratamiento', 'proximo_control']


class ConsumoInsumoSerializer(serializers.ModelSerializer):
    # LAB 8 - EJ 7: NOMBRE del Insumo (otro extremo del N:M) y la @property SUBTOTAL.
    insumo = serializers.CharField(source='insumo.nombre')
    subtotal = serializers.DecimalField(max_digits=9, decimal_places=2,
                                        read_only=True)

    class Meta:
        model = ConsumoInsumo
        fields = ['insumo', 'cantidad', 'precio_unitario', 'subtotal']


class CitaSerializer(serializers.ModelSerializer):
    # LAB 8 - EJ 7: 1:N -> el VETERINARIO COMPLETO en lugar de solo su id.
    veterinario = VeterinarioSerializer(read_only=True)
    # LAB 8 - EJ 7: 1:1 -> la FICHA CLÍNICA; null si la cita aún no fue atendida.
    ficha = FichaClinicaSerializer(read_only=True, allow_null=True)
    # LAB 8 - EJ 7: N:M -> los CONSUMOS del modelo intermedio (cantidad y precio).
    consumos = ConsumoInsumoSerializer(many=True, read_only=True)

    class Meta:
        model = Cita
        fields = ['id', 'mascota', 'dueno', 'servicio', 'fecha', 'hora',
                  'estado', 'veterinario', 'ficha', 'consumos']
