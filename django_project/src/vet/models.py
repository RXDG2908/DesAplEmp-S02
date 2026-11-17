# ==================================================================
# GUIA: ARCHIVO  vet/models.py  (la "M" de MVT: las tablas)
# LAB     : 07 (CitaQuerySet) - Parte 1, app vet. Las tablas ya existian
# EJERCICIO: Lab 07 Ej.1 (campos clave) y Ej.7 (QuerySet)
# QUE HACE : define Veterinario, Insumo, Cita, FichaClinica y ConsumoInsumo.
#           Lab 07 NO crea tablas nuevas: solo agrega CitaQuerySet (con_estado, proximas).
# QUIEN LO USA: ./views.py, ./forms.py, ./serializers.py (Lab 8), ./admin.py
# DOCS    : ../../../docs/guiones/GUION-Lab07-Parte1.md - ../../../docs/exposiciones/EXPOSICION_Lab07_Parte1.md
# ==================================================================
# vet/models.py
# La "M" de MVT: los datos. Cada clase Model = una tabla.
# Relaciones 1:1, 1:N y N:M con through (ya existian; el Lab 07 las reutiliza).

from django.db import models
from django.utils import timezone


class Veterinario(models.Model):
    """Lado "1" de la relacion uno a muchos."""
    nombre = models.CharField(max_length=100)
    colegiatura = models.CharField('N° de colegiatura', max_length=20, unique=True)
    especialidad = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.nombre


# Lab 07 Ej.1: el campo `stock` de aqui es el numero que consumo_registrar descuenta.
class Insumo(models.Model):
    """El otro extremo de la relacion muchos a muchos."""
    nombre = models.CharField(max_length=80, unique=True)
    unidad = models.CharField('Unidad de medida', max_length=20, default='unidad')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

# --- LAB 07, EJERCICIO 7: QuerySet personalizado ---------------------------
# Las reglas de consulta viven en UN solo lugar y se reutilizan en la vista
# (cita_list, reporte) y en la API del Lab 08 (CitaViewSet). Se activa abajo con
# `objects = CitaQuerySet.as_manager()`.
class CitaQuerySet(models.QuerySet):
    # Lab 07 Ej.7: filtra por estado -> Cita.objects.con_estado('Pendiente').
    def con_estado(self, estado):
        return self.filter(estado=estado)

    # Lab 07 Ej.7: citas de hoy en adelante -> Cita.objects.proximas().
    def proximas(self):
        return self.filter(fecha__gte=timezone.localdate())

class Cita(models.Model):
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

    mascota = models.CharField(max_length=100)
    dueno = models.CharField(max_length=100)
    servicio = models.CharField(max_length=20, choices=SERVICIOS)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    # Lab 07 Ej.7: activa el QuerySet propio como manager (Cita.objects.con_estado(...)).
    objects = CitaQuerySet.as_manager()

    # --- UNO A MUCHOS -------------------------------------
    # La FK va aqui porque Cita es el lado "muchos": un veterinario atiende
    # muchas citas, pero cada cita la atiende un solo veterinario.
    # SET_NULL: si un veterinario deja la clinica, su historial de citas NO
    # debe borrarse; la cita queda registrada como "sin asignar".
    # null=True es ademas obligatorio aqui: la tabla ya tenia filas cuando se
    # agrego la columna, y sin null Django pediria un valor por defecto.
    veterinario = models.ForeignKey(
        Veterinario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas',
    )

    # --- MUCHOS A MUCHOS con modelo intermedio ------------
    # La relacion guarda datos propios (cantidad y precio), por eso NO puede
    # ser un M2M simple: necesita el modelo intermedio ConsumoInsumo.
    insumos = models.ManyToManyField(
        Insumo,
        through='ConsumoInsumo',
        related_name='citas',
        blank=True,
    )

    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'


class FichaClinica(models.Model):
    """UNO A UNO: ficha complementaria de la cita.

    Solo existe si la cita fue atendida y, como maximo, una por cita.
    CASCADE: una ficha clinica sin su cita es un dato huerfano; se elimina
    junto con ella.
    """
    cita = models.OneToOneField(
        Cita,
        on_delete=models.CASCADE,
        related_name='ficha',
    )
    peso_kg = models.DecimalField('Peso (kg)', max_digits=5, decimal_places=2)
    diagnostico = models.TextField()
    tratamiento = models.TextField(blank=True)
    proximo_control = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Ficha clínica'
        verbose_name_plural = 'Fichas clínicas'

    def __str__(self):
        return f'Ficha de {self.cita.mascota}'


class ConsumoInsumo(models.Model):
    """Modelo intermedio (through) de Cita <-> Insumo.

    Guarda dos atributos que NO pertenecen ni a Cita ni a Insumo: cuantas
    unidades se usaron y a que precio se cobraron ese dia.
    """
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE,
                             related_name='consumos')
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT,
                               related_name='consumos')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'Consumo de insumo'
        verbose_name_plural = 'Consumos de insumos'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.insumo} x{self.cantidad} en {self.cita.mascota}'
