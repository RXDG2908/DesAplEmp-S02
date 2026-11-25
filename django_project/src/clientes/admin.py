# ==================================================================
# ARCHIVO  : clientes/admin.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : DJANGO ADMIN de la app: Cliente.
# ==================================================================
from django.contrib import admin

from .models import Cliente

admin.site.register(Cliente)
