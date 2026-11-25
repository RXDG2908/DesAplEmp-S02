# ==================================================================
# ARCHIVO  : clientes/api_urls.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : RUTAS de la API de clientes. ../config/urls.py las MONTA bajo /api/.
# ------------------------------------------------------------------
# LAB 14 - EJ 10: /api/clientes/ y /api/clientes/<id>/.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 10 ... línea 16
# ==================================================================
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('clientes', api_views.ClienteViewSet, basename='cliente')

urlpatterns = router.urls
