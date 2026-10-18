# vet/api_urls.py
# Semana 8 - rutas de la API. config/urls.py las monta bajo /api/.

from rest_framework.routers import DefaultRouter

from . import api_views

# Ejercicio 5 - el router genera las rutas de lista y detalle de cada
# ViewSet, y ademas la raiz /api/ con los recursos registrados.
router = DefaultRouter()
router.register('insumos', api_views.InsumoViewSet, basename='insumo')
router.register('citas', api_views.CitaViewSet, basename='cita')

urlpatterns = router.urls

# Ejercicio 4 - version anterior con vistas genericas (reemplazada):
# from django.urls import path
# urlpatterns = [
#     path('insumos/', api_views.InsumoListCreate.as_view()),
#     path('insumos/<int:pk>/', api_views.InsumoDetail.as_view()),
# ]
