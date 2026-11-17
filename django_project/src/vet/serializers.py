# ==================================================================
# GUIA: ARCHIVO  vet/serializers.py  (Model <-> JSON)
# LAB     : 08 (API REST con Django REST Framework) - Parte 1, app vet
# EJERCICIO: Ej.2-3 InsumoSerializer + validate_stock / Ej.7 CitaSerializer anidado
# QUE HACE : es el "Form" de la API: convierte instancias a JSON y valida el JSON entrante.
# QUIEN LO USA: ./api_views.py
# SE PRUEBA: /api/insumos/ - /api/citas/
# DOCS    : ../../../docs/guiones/GUION-Lab08-Parte1.md - ../../../docs/exposiciones/EXPOSICION_Lab08_Parte1.md
# ==================================================================
# vet/serializers.py
# Lab 08 - Django REST Framework.
# Un serializer convierte instancias del Model a JSON (serializar) y valida
# el JSON que llega antes de guardarlo (deserializar). Es el equivalente al
# Form de las Views HTML, pero para la API.

from rest_framework import serializers

from .models import Cita, ConsumoInsumo, FichaClinica, Insumo, Veterinario


# --- Lab 08 Ej.2 y 3: recurso SIMPLE con una regla de negocio ----------
class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ['id', 'nombre', 'unidad', 'stock']

    # Lab 08 Ej.3 - validate_<campo>: DRF lo llama solo dentro de is_valid().
    # Regla de negocio: un insumo se da de alta con al menos una unidad en
    # stock; registrar un insumo sin existencias no tiene sentido en almacen.
    def validate_stock(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'El stock inicial debe ser de al menos 1 unidad.')
        return value


# --- Lab 08 Ej.7: recurso CON RELACIONES (solo lectura, anidado) -------
class VeterinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinario
        fields = ['id', 'nombre', 'colegiatura', 'especialidad']


class FichaClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaClinica
        fields = ['peso_kg', 'diagnostico', 'tratamiento', 'proximo_control']


class ConsumoInsumoSerializer(serializers.ModelSerializer):
    # Datos del Insumo (otro extremo del N:M) y la @property subtotal.
    insumo = serializers.CharField(source='insumo.nombre')
    subtotal = serializers.DecimalField(max_digits=9, decimal_places=2,
                                        read_only=True)

    class Meta:
        model = ConsumoInsumo
        fields = ['insumo', 'cantidad', 'precio_unitario', 'subtotal']


class CitaSerializer(serializers.ModelSerializer):
    # 1:N  -> el veterinario completo en lugar de solo su id.
    veterinario = VeterinarioSerializer(read_only=True)
    # 1:1  -> la ficha clinica; null si la cita aun no fue atendida.
    ficha = FichaClinicaSerializer(read_only=True, allow_null=True)
    # N:M  -> los consumos del modelo intermedio (cantidad y precio).
    consumos = ConsumoInsumoSerializer(many=True, read_only=True)

    class Meta:
        model = Cita
        fields = ['id', 'mascota', 'dueno', 'servicio', 'fecha', 'hora',
                  'estado', 'veterinario', 'ficha', 'consumos']
