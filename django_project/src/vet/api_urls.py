# ==================================================================
# GUIA: ARCHIVO  vet/api_urls.py  (rutas de la API)
# LAB     : 08 (API REST con DRF) - Parte 1, app vet
# EJERCICIO: Ej.5 DefaultRouter genera lista, detalle y la raiz /api/
# QUE HACE : registra InsumoViewSet y CitaViewSet; ../config/urls.py lo monta bajo /api/.
# DOCS    : ../../../docs/guiones/GUION-Lab08-Parte1.md
# ==================================================================
# vet/api_urls.py
# Lab 08 - rutas de la API. ../config/urls.py las monta bajo /api/.

from rest_framework.routers import DefaultRouter

from . import api_views

# Lab 08 Ej.5 - el router genera las rutas de lista y detalle de cada
# ViewSet, y ademas la raiz /api/ con los recursos registrados.
router = DefaultRouter()
router.register('insumos', api_views.InsumoViewSet, basename='insumo')
router.register('citas', api_views.CitaViewSet, basename='cita')

urlpatterns = router.urls

# Lab 08 Ej.4 - version anterior con vistas genericas (reemplazada):
# from django.urls import path
# urlpatterns = [
#     path('insumos/', api_views.InsumoListCreate.as_view()),
#     path('insumos/<int:pk>/', api_views.InsumoDetail.as_view()),
# ]
