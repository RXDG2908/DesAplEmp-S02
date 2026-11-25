# ==================================================================
# ARCHIVO  : servicios/admin.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : DJANGO ADMIN de la app: Rubro.
# ------------------------------------------------------------------
# LAB 14 - EJ 10: registra Rubro para revisar los datos de prueba.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 15
# ==================================================================
from django.contrib import admin

from .models import Rubro

admin.site.register(Rubro)
