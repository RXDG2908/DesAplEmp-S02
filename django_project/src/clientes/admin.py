# ==================================================================
# ARCHIVO  : clientes/admin.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : DJANGO ADMIN de la app: Cliente.
# ------------------------------------------------------------------
# LAB 14 - EJ 10: registra Cliente para revisar los datos de prueba.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 15
# ==================================================================
from django.contrib import admin

from .models import Cliente

admin.site.register(Cliente)
