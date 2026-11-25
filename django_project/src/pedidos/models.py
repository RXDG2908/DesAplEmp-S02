# ==================================================================
# ARCHIVO  : pedidos/models.py
# PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
# ROL      : la "M" de MVT -> TABLAS Cliente, Pedido, DetallePedido y Pago.
# ------------------------------------------------------------------
# LAB 13 - EJ 6: app creada vacía; aquí solo se DISEÑÓ.
# LAB 14 - EJ 4: relaciones con on_delete justificado, dinero en DecimalField
#                y estados con choices (PEN, PAG, ENT, CAN).
# LAB 14 - EJ 8: Pago simulado (un pago por pedido) para el cambio a PAGADO.
# ------------------------------------------------------------------
# USADO EN : ./serializers.py, ./api_views.py, ../cargar_lab14.py
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 13 - EJ 6 .... línea 18
#   LAB 14 - EJ 4 .... líneas 38, 50, 52
#   LAB 14 - EJ 8 .... línea 69
# ==================================================================
from django.db import models

from catalogo.models import Producto


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('PAG', 'Pagado'),
        ('ENT', 'Entregado'),
        ('CAN', 'Cancelado'),
    ]
    # LAB 14 - EJ 4: PROTECT -> no se borra un cliente que tiene pedidos (historial de ventas).
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN')
    # El total lo calcula Django en crear_pedido, nunca el navegador.
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Pedido {self.pk} - {self.cliente} ({self.estado})'


class DetallePedido(models.Model):
    # LAB 14 - EJ 4: CASCADE -> si se borra el pedido, sus líneas no tienen sentido solas.
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    # LAB 14 - EJ 4: PROTECT -> no se borra un producto que ya se vendió.
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    # Se COPIA el precio del momento de la venta para conservar el historial.
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario


class Pago(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    # LAB 14 - EJ 8: OneToOne -> un solo pago por pedido; PROTECT conserva el registro del cobro.
    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT, related_name='pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=20)
    # Solo la REFERENCIA que devuelve la pasarela; nunca el número de tarjeta ni el CVV.
    ref_pasarela = models.CharField(max_length=60, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')
    fecha = models.DateTimeField(auto_now_add=True)
