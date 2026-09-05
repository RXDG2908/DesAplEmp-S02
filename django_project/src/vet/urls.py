# vet/urls.py
# Tabla de rutas PROPIA de la App. El urls.py del Project (config/urls.py)
# incluye este archivo con `include('vet.urls')`, así la App queda montada bajo
# una ruta y sus URLs se definen aquí, no en el Project.

from django.urls import path

from . import views
# Se importan las vistas para poder apuntar cada ruta a su función.

app_name = 'vet'
# Namespace de la App: permite escribir `vet:cita_list` en templates y
# redirects sin chocar con rutas de otras Apps que se llamen igual.

urlpatterns = [
    # path(ruta, vista, name)
    #  - ''        -> raíz de la App: el listado de citas.
    #  - 'nueva/'  -> formulario para registrar una cita.
    # `name` es el identificador interno que se usa en {% url %} y redirect().
    path('', views.cita_list, name='cita_list'),
    path('nueva/', views.cita_crear, name='cita_crear'),
]
