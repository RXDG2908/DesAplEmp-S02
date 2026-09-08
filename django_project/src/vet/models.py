# vet/models.py
# La "M" de MVT: los datos. Cada clase Model = una tabla.

from django.db import models


class Cita(models.Model):
    # Antes era una lista en memoria. Ahora se guarda en SQLite con el ORM.

    # Opciones fijas: van en el codigo, no en una tabla aparte.
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

    # Campos = columnas de la tabla.
    mascota = models.CharField(max_length=100)
    dueno = models.CharField(max_length=100)
    servicio = models.CharField(max_length=20, choices=SERVICIOS)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS,
                              default='Pendiente')

    # Como se muestra la cita en el shell y en el admin.
    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'
