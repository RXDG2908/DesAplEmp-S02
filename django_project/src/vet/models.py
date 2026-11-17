# ==================================================================
# ARCHIVO  : vet/models.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : la "M" de MVT -> cada clase Model es una TABLA.
# ------------------------------------------------------------------
# LAB 7 - EJ 1: CAMPOS CLAVE -> Insumo.stock (lo que se DESCUENTA) y Cita.estado.
# LAB 7 - EJ 7: QUERYSET PERSONALIZADO CitaQuerySet (con_estado, proximas).
# NOTA     : el Lab 7 NO crea tablas nuevas; reutiliza las relaciones
#            1:1, 1:N y N:M (con through) que ya existían desde el Lab 4.
# ------------------------------------------------------------------
# USADO EN : ./views.py, ./forms.py, ./serializers.py, ./api_views.py, ./admin.py
# DOCS     : ../../../docs/guiones/GUION-Lab07-Parte1.md
#            ../../../docs/exposiciones/EXPOSICION_Lab07_Parte1.md
# ==================================================================

from django.db import models
from django.utils import timezone


class Veterinario(models.Model):
    """Lado "1" de la relación UNO A MUCHOS (un veterinario, muchas citas)."""
    nombre = models.CharField(max_length=100)
    colegiatura = models.CharField('N° de colegiatura', max_length=20, unique=True)
    especialidad = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.nombre


# LAB 7 - EJ 1: el campo STOCK es el número que consumo_registrar DESCUENTA con F().
class Insumo(models.Model):
    """El otro extremo de la relación MUCHOS A MUCHOS con Cita."""
    nombre = models.CharField(max_length=80, unique=True)
    unidad = models.CharField('Unidad de medida', max_length=20, default='unidad')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

# --- LAB 7 - EJ 7: QUERYSET PERSONALIZADO ---------------------------------
# Las REGLAS DE CONSULTA viven en UN SOLO LUGAR y se REUTILIZAN en las vistas
# (cita_list, reporte) y en la API del Lab 8 (CitaViewSet).
# Se activa más abajo con: objects = CitaQuerySet.as_manager()
# Los métodos son ENCADENABLES: Cita.objects.proximas().con_estado('Pendiente')
class CitaQuerySet(models.QuerySet):
    # LAB 7 - EJ 7: FILTRA POR ESTADO -> Cita.objects.con_estado('Pendiente').
    def con_estado(self, estado):
        return self.filter(estado=estado)

    # LAB 7 - EJ 7: citas de HOY EN ADELANTE -> Cita.objects.proximas().
    def proximas(self):
        return self.filter(fecha__gte=timezone.localdate())

class Cita(models.Model):
    # OPCIONES FIJAS (choices): van en el código, no en una tabla aparte.
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
    # LAB 7 - EJ 7: ACTIVA el QuerySet propio como MANAGER -> Cita.objects.con_estado(...).
    objects = CitaQuerySet.as_manager()

    # --- UNO A MUCHOS (1:N) -------------------------------
    # La FOREIGN KEY va aquí porque Cita es el lado "MUCHOS": un veterinario
    # atiende muchas citas, pero cada cita la atiende un solo veterinario.
    # SET_NULL: si un veterinario deja la clínica, su historial de citas NO
    # se borra; la cita queda registrada como "sin asignar".
    # null=True es además OBLIGATORIO: la tabla ya tenía filas cuando se
    # agregó la columna y, sin null, Django pediría un valor por defecto.
    veterinario = models.ForeignKey(
        Veterinario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas',
    )

    # --- MUCHOS A MUCHOS (N:M) con MODELO INTERMEDIO ------
    # La relación guarda DATOS PROPIOS (cantidad y precio); por eso NO puede
    # ser un M2M simple: necesita el modelo intermedio ConsumoInsumo (through).
    insumos = models.ManyToManyField(
        Insumo,
        through='ConsumoInsumo',
        related_name='citas',
        blank=True,
    )

    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'


class FichaClinica(models.Model):
    """UNO A UNO (1:1): ficha complementaria de la cita.

    Solo existe si la cita fue ATENDIDA y, como máximo, hay UNA por cita.
    CASCADE: una ficha clínica sin su cita es un dato huérfano; se elimina
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
    """MODELO INTERMEDIO (through) de Cita <-> Insumo.

    Guarda dos atributos que NO pertenecen ni a Cita ni a Insumo: CUÁNTAS
    unidades se usaron y a QUÉ PRECIO se cobraron ese día.
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
