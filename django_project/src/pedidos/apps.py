# ==================================================================
# ARCHIVO  : pedidos/apps.py
# PARTE 1  : PRÁCTICA (Lucas): tienda en línea de la CAFETERÍA
# ROL      : CONFIGURACIÓN de la APP 'pedidos' (name = 'pedidos').
# ------------------------------------------------------------------
# LAB 13 - EJ 6: APP creada con 'python manage.py startapp pedidos' y registrada en config/settings.py.
#                Tema: PEDIDOS de la cafetería: el pedido con estado (PEN, PAG, ENT) y su detalle.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 13 - EJ 6 .... línea 15
# ==================================================================
from django.apps import AppConfig


class PedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedidos'
