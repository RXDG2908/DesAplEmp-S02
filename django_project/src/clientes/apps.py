# ==================================================================
# ARCHIVO  : clientes/apps.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : CONFIGURACIÓN de la APP 'clientes' (name = 'clientes').
# ------------------------------------------------------------------
# LAB 13 - EJ 12: APP creada con 'python manage.py startapp clientes' y registrada en config/settings.py.
#                 Tema: CLIENTES que piden servicios a los prestadores.
# ==================================================================
from django.apps import AppConfig


class ClientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientes'
