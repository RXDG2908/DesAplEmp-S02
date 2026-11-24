# ==================================================================
# ARCHIVO  : config/urls.py
# ROL      : ENRUTADOR RAÍZ del Project ("director de tráfico"):
#            /                -> vet.urls (páginas HTML de la VETERINARIA)
#            /biblioteca/     -> biblioteca.urls (Parte 2)
#            /api/            -> API de VET
#            /api/biblioteca/ -> API de la biblioteca (Parte 2)
#            /api/chamba/     -> API de CHAMBA PE
#            /admin/          -> Django Admin
# ------------------------------------------------------------------
# LAB 8 - EJ 4 y 5: monta la API de vet bajo /api/.
# LAB 12 - EJ 9   : monta la API de CHAMBA PE bajo /api/chamba/.
# NOTA     : las rutas /api/... van ANTES de '' para que no las capture vet.urls.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 8 - EJ 4 ..... línea 43
#   LAB 8 - EJ 5 ..... línea 43
#   LAB 12 - EJ 9 .... línea 42
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
    path('api/', include('vet.api_urls')),  # LAB 8 - EJ 5: API REST de VET
    path('', include('vet.urls')),
    path('biblioteca/', include('biblioteca.urls')),
]