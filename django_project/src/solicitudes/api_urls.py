# ==================================================================
# ARCHIVO  : solicitudes/api_urls.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : RUTAS de la API de solicitudes. ../config/urls.py las MONTA bajo /api/.
# ------------------------------------------------------------------
# LAB 14 - EJ 11: el router genera /solicitudes/, /solicitudes/<id>/ y la acción
#                 /solicitudes/<id>/avanzar/.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 11 ... línea 17
# ==================================================================
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('solicitudes', api_views.SolicitudViewSet, basename='solicitud')

urlpatterns = router.urls
