# ==================================================================
# ARCHIVO  : solicitudes/apps.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : CONFIGURACIÓN de la APP 'solicitudes' (name = 'solicitudes').
# ------------------------------------------------------------------
# LAB 13 - EJ 12: APP creada con 'python manage.py startapp solicitudes' y registrada en config/settings.py.
#                 Tema: SOLICITUDES DE SERVICIO (operación principal) y su seguimiento.
# ==================================================================
from django.apps import AppConfig


class SolicitudesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'solicitudes'
