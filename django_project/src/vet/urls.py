# vet/urls.py
# Rutas de la App. config/urls.py incluye este archivo.

from django.urls import path

from . import views

# Namespace: permite escribir vet:cita_list en templates y redirects.
app_name = 'vet'

urlpatterns = [
    # /        -> listado de citas
    # /nueva/  -> formulario para registrar
    path('', views.cita_list, name='cita_list'),
    path('nueva/', views.cita_crear, name='cita_crear'),
]
