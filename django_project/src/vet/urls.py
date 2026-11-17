# ==================================================================
# GUIA: ARCHIVO  vet/urls.py  (rutas HTML de la app vet)
# LAB     : 07 (consumo y reporte) - Parte 1; las demas rutas ya existian
# EJERCICIO: Lab 07 Ej.3 -> consumo/nuevo/ - Ej.6 -> reporte/
# QUE HACE : enlaza cada URL con su vista de ./views.py. ../config/urls.py monta este archivo en '/'.
# DOCS    : ../../../docs/guiones/GUION-Lab07-Parte1.md
# ==================================================================
# vet/urls.py
# Rutas de la App. ../config/urls.py incluye este archivo.

from django.urls import path

from . import views

# Namespace: permite escribir vet:cita_list en templates y redirects.
app_name = 'vet'

urlpatterns = [
    # /        -> listado de citas
    # /nueva/  -> formulario para registrar
    path('', views.cita_list, name='cita_list'),
    path('nueva/', views.cita_crear, name='cita_crear'),
    # Detalle con los datos relacionados (1:1, 1:N y el intermedio).
    path('cita/<int:pk>/', views.cita_detalle, name='cita_detalle'),
    # Lab 07 Ej.3: formulario que registra el consumo dentro de una transaccion.
    # Lab 07 Ej.6: pagina de reporte con aggregate() y annotate().
    path('consumo/nuevo/', views.consumo_registrar, name='consumo_registrar'),
    path('reporte/', views.reporte, name='reporte'),
]
