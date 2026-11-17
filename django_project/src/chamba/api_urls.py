# ==================================================================
# ARCHIVO  : chamba/api_urls.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : RUTAS DE LA API. ../config/urls.py las MONTA bajo /api/chamba/.
# ------------------------------------------------------------------
# LAB 12 - EJ 9: el DEFAULTROUTER genera /prestadores/ (lista) y /prestadores/<id>/ (detalle).
# ==================================================================

from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('prestadores', api_views.PrestadorViewSet, basename='prestador')

urlpatterns = router.urls
