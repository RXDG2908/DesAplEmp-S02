# ==================================================================
# ARCHIVO  : pedidos/api_views.py
# PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
# ROL      : CONTROLADORES de pedidos: consulta, CREAR PEDIDO con reglas y PAGO SIMULADO.
# ------------------------------------------------------------------
# LAB 14 - EJ 8: crear_pedido -> transaction.atomic, stock descontado con F(),
#                precio tomado de la BD y total calculado en el servidor.
#                Responde 201 si todo sale bien y 400 (sin tocar el stock) si falta stock.
# LAB 14 - EJ 8: confirmar_pago -> registra un Pago simulado y deja el pedido en PAG.
# ------------------------------------------------------------------
# USADO EN : ./api_urls.py
# SE PRUEBA: POST /api/pedidos/crear/  ·  POST /api/pedidos/<id>/pagar/
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 8 .... líneas 49, 59
# ==================================================================
from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from catalogo.models import Producto

from .models import Cliente, DetallePedido, Pago, Pedido
from .serializers import PedidoSerializer


class PedidoViewSet(viewsets.ReadOnlyModelViewSet):
    # Los pedidos NO se crean por aquí: se crean con crear_pedido, que aplica las reglas.
    queryset = (Pedido.objects.select_related('cliente', 'pago')
                .prefetch_related('detalles__producto').order_by('-id'))
    serializer_class = PedidoSerializer


@api_view(['POST'])
def crear_pedido(request):
    """Body: {"cliente_id": 1, "items": [{"producto_id": 2, "cantidad": 3}, ...]}"""
    items = request.data.get('items') or []
    if not items:
        raise ValidationError({'items': 'El pedido debe tener al menos un producto.'})
    cliente = Cliente.objects.filter(pk=request.data.get('cliente_id')).first()
    if cliente is None:
        raise ValidationError({'cliente_id': 'El cliente no existe.'})

    # LAB 14 - EJ 8: TODO O NADA -> si un producto no tiene stock, se deshace el pedido
    # completo y también los descuentos de stock ya hechos.
    with transaction.atomic():
        pedido = Pedido.objects.create(cliente=cliente)
        total = Decimal('0')
        for item in items:
            producto = Producto.objects.filter(pk=item.get('producto_id'), activo=True).first()
            cantidad = int(item.get('cantidad', 0))
            if producto is None or cantidad < 1:
                raise ValidationError({'items': 'Producto o cantidad no válidos.'})
            # LAB 14 - EJ 8: F('stock') - cantidad resta DENTRO de la base de datos, y solo
            # si alcanza el stock (stock__gte); 0 filas = no alcanzó.
            filas = (Producto.objects.filter(pk=producto.pk, stock__gte=cantidad)
                     .update(stock=F('stock') - cantidad))
            if filas == 0:
                raise ValidationError({'stock': f'Stock insuficiente de {producto.nombre}.'})
            # El precio sale de la BASE DE DATOS, no de lo que envía el navegador.
            DetallePedido.objects.create(pedido=pedido, producto=producto,
                                         cantidad=cantidad, precio_unitario=producto.precio)
            total += producto.precio * cantidad
        pedido.total = total
        pedido.save()
    return Response(PedidoSerializer(pedido).data, status=201)


@api_view(['POST'])
def confirmar_pago(request, pedido_id):
    """Pago SIMULADO: no hay pasarela real (se integra en la Semana 16)."""
    with transaction.atomic():
        # select_for_update bloquea el pedido mientras se paga: evita pagarlo dos veces.
        pedido = Pedido.objects.select_for_update().filter(pk=pedido_id).first()
        if pedido is None:
            return Response({'detail': 'El pedido no existe.'}, status=404)
        if pedido.estado != 'PEN':
            raise ValidationError({'estado': 'Solo se puede pagar un pedido Pendiente.'})
        Pago.objects.create(pedido=pedido, monto=pedido.total,
                            metodo=request.data.get('metodo', 'Yape'),
                            ref_pasarela='SIMULADO-' + str(pedido.pk), estado='APROBADO')
        pedido.estado = 'PAG'
        pedido.save()
    return Response(PedidoSerializer(pedido).data)
