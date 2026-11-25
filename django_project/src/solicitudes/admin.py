# ==================================================================
# ARCHIVO  : solicitudes/admin.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : DJANGO ADMIN de la app: Solicitud (con su seguimiento).
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
