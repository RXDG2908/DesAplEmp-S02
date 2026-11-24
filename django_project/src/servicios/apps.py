# ==================================================================
# ARCHIVO  : servicios/apps.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : CONFIGURACIÓN de la APP 'servicios' (name = 'servicios').
# ------------------------------------------------------------------
# LAB 13 - EJ 12: APP creada con 'python manage.py startapp servicios' y registrada en config/settings.py.
#                 Tema: CATÁLOGO DE RUBROS y servicios que ofrecen los prestadores.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 13 - EJ 12 ... línea 15
# ==================================================================
from django.apps import AppConfig


class ServiciosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servicios'
