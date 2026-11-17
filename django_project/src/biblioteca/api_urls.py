# ==================================================================
# GUIA: ARCHIVO  biblioteca/api_urls.py
# LAB     : 08 Parte 2
# QUE HACE : el router genera las rutas de la API; ../config/urls.py las monta en /api/biblioteca/.
# ==================================================================
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('categorias', api_views.CategoriaViewSet, basename='categoria')
router.register('libros', api_views.LibroViewSet, basename='libro')
router.register('prestamos', api_views.PrestamoViewSet, basename='prestamo')

urlpatterns = router.urls