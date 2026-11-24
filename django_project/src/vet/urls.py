# ==================================================================
# ARCHIVO  : vet/urls.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : RUTAS HTML -> enlaza cada URL con su vista de ./views.py.
#            ../config/urls.py MONTA este archivo en '/'.
# ------------------------------------------------------------------
# LAB 7 - EJ 3: ruta consumo/nuevo/ -> TRANSACCIÓN del consumo.
# LAB 7 - EJ 6: ruta reporte/       -> PÁGINA DE REPORTE.
# NOTA     : las rutas de listado, nueva cita y detalle ya existían.
# ------------------------------------------------------------------
# DOCS     : ../../../docs/guiones/GUION-Lab07-Parte1.md
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 7 - EJ 3 ..... línea 32
#   LAB 7 - EJ 6 ..... línea 34
# ==================================================================

from django.urls import path

from . import views

# NAMESPACE: permite escribir vet:cita_list en templates y redirects.
app_name = 'vet'

urlpatterns = [
    # /        -> LISTADO de citas
    # /nueva/  -> FORMULARIO para registrar una cita
    path('', views.cita_list, name='cita_list'),
    path('nueva/', views.cita_crear, name='cita_crear'),
    # DETALLE con los datos relacionados (1:1, 1:N y el modelo intermedio).
    path('cita/<int:pk>/', views.cita_detalle, name='cita_detalle'),
    # LAB 7 - EJ 3: FORMULARIO que registra el consumo dentro de una TRANSACCIÓN.
    path('consumo/nuevo/', views.consumo_registrar, name='consumo_registrar'),
    # LAB 7 - EJ 6: PÁGINA DE REPORTE con aggregate() y annotate().
    path('reporte/', views.reporte, name='reporte'),
]
