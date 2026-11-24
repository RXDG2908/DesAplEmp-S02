# ==================================================================
# ARCHIVO  : catalogo/apps.py
# PARTE 1  : PRÁCTICA (Lucas): tienda en línea de la CAFETERÍA
# ROL      : CONFIGURACIÓN de la APP 'catalogo' (name = 'catalogo').
# ------------------------------------------------------------------
# LAB 13 - EJ 6: APP creada con 'python manage.py startapp catalogo' y registrada en config/settings.py.
#                Tema: CATÁLOGO de la cafetería: productos con precio, categoría y stock.
# ==================================================================
from django.apps import AppConfig


class CatalogoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogo'
