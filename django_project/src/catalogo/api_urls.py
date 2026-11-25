# ==================================================================
# ARCHIVO  : catalogo/api_urls.py
# PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
# ROL      : RUTAS de la API del catálogo. ../config/urls.py las MONTA bajo /api/.
# ------------------------------------------------------------------
# LAB 14 - EJ 6: el DEFAULTROUTER genera /productos/ (lista) y /productos/<id>/
#                (detalle), lo mismo para /categorias/, y la RAÍZ /api/.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 6 .... línea 17
# ==================================================================
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('productos', api_views.ProductoViewSet, basename='producto')
router.register('categorias', api_views.CategoriaViewSet, basename='categoria')

urlpatterns = router.urls
