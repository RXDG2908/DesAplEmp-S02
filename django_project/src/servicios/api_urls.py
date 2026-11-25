# ==================================================================
# ARCHIVO  : servicios/api_urls.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : RUTAS de la API de rubros. ../config/urls.py las MONTA bajo /api/servicios/.
# ------------------------------------------------------------------
# LAB 14 - EJ 10: /api/servicios/rubros/ (la ruta del mapa del Lab 13).
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 16
# ==================================================================
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('rubros', api_views.RubroViewSet, basename='rubro')

urlpatterns = router.urls
