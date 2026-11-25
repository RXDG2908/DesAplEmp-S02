# ==================================================================
# ARCHIVO  : config/urls.py
# ROL      : ENRUTADOR RAÍZ del Project ("director de tráfico"):
#            /                -> vet.urls (páginas HTML de la VETERINARIA)
#            /biblioteca/     -> biblioteca.urls (Parte 2)
#            /api/            -> APIs de VET, de la CAFETERÍA (catálogo y pedidos) y de
#                                CHAMBA PE (clientes y solicitudes)
#            /api/servicios/  -> rubros de CHAMBA PE
#            /api/biblioteca/ -> API de la biblioteca (Parte 2)
#            /api/chamba/     -> API de CHAMBA PE
#            /admin/          -> Django Admin
# ------------------------------------------------------------------
# LAB 8 - EJ 4 y 5: monta la API de vet bajo /api/.
# LAB 12 - EJ 9   : monta la API de CHAMBA PE bajo /api/chamba/.
# LAB 14 - EJ 6   : monta la API del catálogo (productos, categorias) bajo /api/.
# LAB 14 - EJ 8   : monta pedidos, /pedidos/crear/ y /pedidos/<id>/pagar/ bajo /api/.
# LAB 14 - EJ 10  : monta rubros (/api/servicios/) y clientes (/api/) de CHAMBA PE.
# LAB 14 - EJ 11  : monta solicitudes y /solicitudes/<id>/avanzar/ bajo /api/.
# NOTA     : las rutas /api/... van ANTES de '' para que no las capture vet.urls.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 8 - EJ 4 ..... línea 58
#   LAB 8 - EJ 5 ..... línea 58
#   LAB 12 - EJ 9 .... línea 52
#   LAB 14 - EJ 6 .... línea 54
#   LAB 14 - EJ 8 .... línea 55
#   LAB 14 - EJ 10 ... líneas 53, 56
#   LAB 14 - EJ 11 ... línea 57
# ==================================================================
"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/biblioteca/', include('biblioteca.api_urls')),
    path('api/chamba/', include('chamba.api_urls')),  # LAB 12 - EJ 9: API de CHAMBA PE
    path('api/servicios/', include('servicios.api_urls')),  # LAB 14 - EJ 10: rubros de CHAMBA PE
    path('api/', include('catalogo.api_urls')),  # LAB 14 - EJ 6: productos y categorias (CAFETERIA)
    path('api/', include('pedidos.api_urls')),  # LAB 14 - EJ 8: pedidos y pago simulado (CAFETERIA)
    path('api/', include('clientes.api_urls')),  # LAB 14 - EJ 10: clientes de CHAMBA PE
    path('api/', include('solicitudes.api_urls')),  # LAB 14 - EJ 11: solicitudes de CHAMBA PE
    path('api/', include('vet.api_urls')),  # LAB 8 - EJ 5: API REST de VET
    path('', include('vet.urls')),
    path('biblioteca/', include('biblioteca.urls')),
]