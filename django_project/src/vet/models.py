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
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'hora'], name='cita_horario_unico',
            ),
        ]

    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'


# Compatibilidad: la lista de ejemplo de la Semana 2 se conserva como datos
# de carga inicial (ver data migration 0002). Ya no es la fuente de datos.
SERVICIOS = [s[0] for s in Cita.SERVICIOS]
ESTADOS = [e[0] for e in Cita.ESTADOS]
