# ==================================================================
# ARCHIVO  : chamba/models.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : la "M" de MVT -> define la TABLA Prestador.
# ------------------------------------------------------------------
# LAB 12 - EJ 9: PRESTADOR = ENTIDAD PRINCIPAL del panel administrativo.
#                Se creó para que el panel del Lab 11 (datos a mano) pase a
#                leer y escribir en una API REAL.
# ------------------------------------------------------------------
# USADO EN : ./serializers.py, ./api_views.py, ./admin.py, ../cargar_chamba.py
# ==================================================================

from django.db import models


class Prestador(models.Model):
    # OPCIONES FIJAS (choices): los mismos valores del <select> de PrestadorForm.jsx.
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
