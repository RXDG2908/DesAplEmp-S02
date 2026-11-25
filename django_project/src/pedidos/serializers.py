# ==================================================================
# ARCHIVO  : pedidos/serializers.py
# PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
# ROL      : MODEL <-> JSON de los pedidos con sus líneas y su pago (solo lectura).
# ------------------------------------------------------------------
# LAB 14 - EJ 8: el pedido se devuelve con sus DETALLES y el total calculado en Django.
# ------------------------------------------------------------------
# USADO EN : ./api_views.py
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 8 .... línea 33
# ==================================================================
from rest_framework import serializers

from .models import DetallePedido, Pago, Pedido


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto = serializers.CharField(source='producto.nombre')
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['monto', 'metodo', 'ref_pasarela', 'estado', 'fecha']


class PedidoSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(source='cliente.nombre')
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    pago = PagoSerializer(read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'fecha', 'estado', 'total', 'detalles', 'pago']
