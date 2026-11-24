# ==================================================================
# ARCHIVO  : vet/apps.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : CONFIGURACIÓN de la APP 'vet'; va registrada en INSTALLED_APPS (config/settings.py).
# ==================================================================

from django.apps import AppConfig


class VetConfig(AppConfig):
    # Tipo del campo id que Django agrega solo.
    default_auto_field = 'django.db.models.BigAutoField'
    # Nombre interno (igual a la carpeta).
    name = 'vet'
    # Nombre que se ve en el admin.
    verbose_name = 'Citas veterinaria'
