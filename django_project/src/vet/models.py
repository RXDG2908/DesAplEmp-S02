from django.db import models


class Cita(models.Model):
    """Cita de la veterinaria, ahora persistida en SQLite mediante el ORM."""

    # ¿Por qué SERVICIOS y ESTADOS viven en el código y no en una tabla?
    #
    # Son catálogos CERRADOS: la veterinaria ofrece un conjunto fijo de 4
    # servicios y una cita solo puede estar en 3 estados. No los da de alta el
    # usuario, no cambian mientras el servidor corre y no tienen datos propios
    # (precio, duración, etc.), solo el nombre. Por eso NO se crea una tabla
    # aparte: se usan como `choices` del campo, que es lo que Django recomienda
    # para listas de opciones fijas. Django los aprovecha para validar el valor
    # guardado y para armar el desplegable del formulario.
    #
    # Si algún día hubiera que administrarlos (agregar/quitar servicios,
    # ponerles precio), recién ahí se convertirían en un modelo `Servicio` con
    # relación `ForeignKey` hacia `Cita`.
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
