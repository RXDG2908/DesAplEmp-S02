# ==================================================================
# ARCHIVO  : clientes/models.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : la "M" de MVT -> TABLA Cliente (quien pide un servicio).
# ------------------------------------------------------------------
# LAB 13 - EJ 12: app creada vacía; aquí solo se DISEÑÓ.
# LAB 14 - EJ 10: modelo Cliente con sus datos de contacto.
# ------------------------------------------------------------------
# USADO EN : ./serializers.py, ../solicitudes/models.py, ../cargar_lab14.py
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 13 - EJ 12 ... línea 15
#   LAB 14 - EJ 10 ... línea 18
# ==================================================================
from django.db import models


class Cliente(models.Model):
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
