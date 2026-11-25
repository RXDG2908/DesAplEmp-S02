# ==================================================================
# ARCHIVO  : solicitudes/admin.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : DJANGO ADMIN de la app: Solicitud (con su seguimiento).
# ------------------------------------------------------------------
# LAB 14 - EJ 10: muestra cada Solicitud con su seguimiento (inline) y filtros por estado y rubro.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 22
# ==================================================================
from django.contrib import admin

from .models import SeguimientoSolicitud, Solicitud


class SeguimientoInline(admin.TabularInline):
    model = SeguimientoSolicitud
    extra = 0


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'prestador', 'rubro', 'estado', 'monto']
    list_filter = ['estado', 'rubro']
    inlines = [SeguimientoInline]
