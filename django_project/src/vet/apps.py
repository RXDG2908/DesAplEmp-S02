from django.apps import AppConfig


class VetConfig(AppConfig):
    """Configuración de la app de reserva de citas de la veterinaria."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vet'
    verbose_name = 'Citas veterinaria'
