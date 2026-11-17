# ==================================================================
# ARCHIVO  : vet/api_urls.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : RUTAS DE LA API. ../config/urls.py las MONTA bajo /api/.
# ------------------------------------------------------------------
# LAB 8 - EJ 4: rutas manuales de las VISTAS GENÉRICAS (comentadas al final).
# LAB 8 - EJ 5: DEFAULTROUTER -> genera LISTA, DETALLE y la RAÍZ /api/.
# ------------------------------------------------------------------
# DOCS     : ../../../docs/guiones/GUION-Lab08-Parte1.md
# ==================================================================

from rest_framework.routers import DefaultRouter

from . import api_views

# LAB 8 - EJ 5: el ROUTER genera las rutas de LISTA y DETALLE de cada
# ViewSet, y además la RAÍZ /api/ con los recursos registrados.
router = DefaultRouter()
router.register('insumos', api_views.InsumoViewSet, basename='insumo')
router.register('citas', api_views.CitaViewSet, basename='cita')

urlpatterns = router.urls

# LAB 8 - EJ 4: VERSIÓN ANTERIOR con vistas genéricas (REEMPLAZADA por el router):
# from django.urls import path
# urlpatterns = [
#     path('insumos/', api_views.InsumoListCreate.as_view()),
#     path('insumos/<int:pk>/', api_views.InsumoDetail.as_view()),
# ]
