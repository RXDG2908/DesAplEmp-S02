from django.db import models


class Cita(models.Model):
    """Cita de la veterinaria, ahora persistida en SQLite mediante el ORM."""

    SERVICIOS = [
        ('Consulta', 'Consulta'),
        ('Vacunación', 'Vacunación'),
        ('Cirugía', 'Cirugía'),
        ('Baño', 'Baño'),
    ]

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Atendida', 'Atendida'),
    ]

    mascota = models.CharField('Mascota', max_length=100)
    dueno = models.CharField('Dueño', max_length=100)
    servicio = models.CharField('Servicio', max_length=20, choices=SERVICIOS)
    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')
    estado = models.CharField(
        'Estado', max_length=20, choices=ESTADOS, default='Pendiente',
    )

    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'