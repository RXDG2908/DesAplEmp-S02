# ==================================================================
# ARCHIVO  : solicitudes/models.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : la "M" de MVT -> Solicitud (ENTIDAD PRINCIPAL) y SeguimientoSolicitud (DETALLE).
# ------------------------------------------------------------------
# LAB 13 - EJ 12: app creada vacía; aquí solo se DISEÑÓ.
# LAB 14 - EJ 10: Solicitud con FK a Cliente, Prestador y Rubro (on_delete justificado)
#                 y la tabla de DETALLE SeguimientoSolicitud (un registro por cambio de estado).
# LAB 14 - EJ 11: el monto se COPIA de la tarifa del prestador al crear la solicitud.
# ------------------------------------------------------------------
# USADO EN : ./serializers.py, ./api_views.py, ../cargar_lab14.py
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 13 - EJ 12 ... línea 18
#   LAB 14 - EJ 10 ... líneas 39, 59
#   LAB 14 - EJ 11 ... línea 48
# ==================================================================
from django.db import models

from chamba.models import Prestador
from clientes.models import Cliente
from servicios.models import Rubro


class Solicitud(models.Model):
    # Los estados avanzan EN ESTE ORDEN (ver Solicitud.SIGUIENTE).
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('CON', 'Confirmada'),
        ('CAM', 'En camino'),
        ('SER', 'En servicio'),
        ('FIN', 'Finalizada'),
        ('PAG', 'Pagada'),
        ('CAN', 'Cancelada'),
    ]
    SIGUIENTE = {'PEN': 'CON', 'CON': 'CAM', 'CAM': 'SER', 'SER': 'FIN', 'FIN': 'PAG'}
    EN_CURSO = ['CON', 'CAM', 'SER']

    # LAB 14 - EJ 10: PROTECT en las tres FK -> no se puede borrar un cliente, un prestador
    # ni un rubro que ya tiene solicitudes: se perdería el historial de servicios y pagos.
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='solicitudes')
    prestador = models.ForeignKey(Prestador, on_delete=models.PROTECT, related_name='solicitudes')
    rubro = models.ForeignKey(Rubro, on_delete=models.PROTECT, related_name='solicitudes')
    direccion = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN')
    # LAB 14 - EJ 11: Decimal y COPIADO de Prestador.tarifa por Django (nunca del navegador).
    monto = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f'Solicitud {self.pk}: {self.rubro} para {self.cliente} ({self.estado})'


class SeguimientoSolicitud(models.Model):
    # LAB 14 - EJ 10: CASCADE -> el seguimiento solo existe dentro de su solicitud.
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='seguimiento')
    estado = models.CharField(max_length=3, choices=Solicitud.ESTADOS)
    fecha = models.DateTimeField(auto_now_add=True)
    nota = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['fecha', 'id']
