# ==================================================================
# ARCHIVO  : pedidos/admin.py
# PARTE 1  : PRÁCTICA (Lucas): tienda en línea de la CAFETERÍA
# ROL      : DJANGO ADMIN de la app: Pedido (con sus líneas), Cliente y Pago.
# ==================================================================
from django.contrib import admin

from .models import Cliente, DetallePedido, Pago, Pedido


class DetalleInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'estado', 'total', 'fecha']
    inlines = [DetalleInline]


admin.site.register(Cliente)
admin.site.register(Pago)
