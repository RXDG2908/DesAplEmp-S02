# vet/apps.py
# Configuración de la App. Django crea este archivo con `startapp` y lo
# registra en INSTALLED_APPS (config/settings.py) como 'vet'.

from django.apps import AppConfig


class VetConfig(AppConfig):
    """Configuración de la app de reserva de citas de la veterinaria."""

    # Tipo de clave primaria que Django agrega solo (el campo `id`) a cada
    # modelo que no defina una: BigAutoField = entero grande autoincremental.
    default_auto_field = 'django.db.models.BigAutoField'
    # Nombre interno de la App: tiene que coincidir con la carpeta y con lo
    # que se pone en INSTALLED_APPS.
    name = 'vet'
    # Nombre "bonito" que se muestra en el panel de administración.
    verbose_name = 'Citas veterinaria'
