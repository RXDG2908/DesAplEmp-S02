# ==================================================================
# ARCHIVO  : pedidos/api_urls.py
# PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
# ROL      : RUTAS de la API de pedidos. ../config/urls.py las MONTA bajo /api/.
# ------------------------------------------------------------------
# LAB 14 - EJ 6: el router genera /pedidos/ y /pedidos/<id>/ (solo lectura).
# LAB 14 - EJ 8: rutas propias /pedidos/crear/ y /pedidos/<id>/pagar/.
# NOTA     : las rutas propias van ANTES del router; si no, 'crear' se tomaría como un <id>.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 6 .... línea 20
#   LAB 14 - EJ 8 .... línea 23
# ==================================================================
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('pedidos', api_views.PedidoViewSet, basename='pedido')

urlpatterns = [
    path('pedidos/crear/', api_views.crear_pedido, name='crear_pedido'),
    path('pedidos/<int:pedido_id>/pagar/', api_views.confirmar_pago, name='confirmar_pago'),
] + router.urls
