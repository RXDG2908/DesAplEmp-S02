# ==================================================================
# ARCHIVO  : servicios/admin.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : DJANGO ADMIN de la app: Rubro.
# ==================================================================
from django.contrib import admin

from .models import Rubro

admin.site.register(Rubro)
