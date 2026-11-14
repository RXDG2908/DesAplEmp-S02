# chamba/models.py
# Prestador de Chamba PE: la entidad principal del panel administrativo.

from django.db import models


class Prestador(models.Model):
    RUBROS = [
        ('Gasfitería', 'Gasfitería'),
        ('Electricidad', 'Electricidad'),
        ('Costura', 'Costura'),
        ('Carpintería', 'Carpintería'),
        ('Primeros auxilios', 'Primeros auxilios'),
    ]
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Suspendido', 'Suspendido'),
    ]

    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    rubro = models.CharField(max_length=30, choices=RUBROS)
    tarifa = models.DecimalField('Tarifa por visita (S/)', max_digits=7, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    class Meta:
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.nombres} {self.apellidos} ({self.rubro})'
