# vet/apps.py
# Configuracion de la App. Va registrada en INSTALLED_APPS como 'vet'.

from django.apps import AppConfig


class VetConfig(AppConfig):
    # Tipo del campo id que Django agrega solo.
    default_auto_field = 'django.db.models.BigAutoField'
    # Nombre interno (igual a la carpeta).
    name = 'vet'
    # Nombre que se ve en el admin.
    verbose_name = 'Citas veterinaria'
