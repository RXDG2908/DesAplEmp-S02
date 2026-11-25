# ==================================================================
# ARCHIVO  : servicios/models.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : la "M" de MVT -> TABLA Rubro (el catálogo de servicios que se pueden pedir).
# ------------------------------------------------------------------
# LAB 13 - EJ 12: app creada vacía; aquí solo se DISEÑÓ.
# LAB 14 - EJ 10: modelo Rubro (gasfitería, electricidad, costura, ...).
# ------------------------------------------------------------------
# USADO EN : ./serializers.py, ../solicitudes/models.py, ../cargar_lab14.py
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 13 - EJ 12 ... línea 15
#   LAB 14 - EJ 10 ... línea 18
# ==================================================================
from django.db import models


class Rubro(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    descripcion = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
