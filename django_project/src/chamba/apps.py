# ==================================================================
# ARCHIVO  : chamba/apps.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : CONFIGURACIÓN de la APP 'chamba' (prestadores); registrada en INSTALLED_APPS.
# ==================================================================
from django.apps import AppConfig


class ChambaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chamba'
