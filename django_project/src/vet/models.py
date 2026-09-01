# vet/models.py
# Aquí se define la capa de DATOS de la App (la "M" de MVT). Cada clase que
# hereda de models.Model se convierte en una tabla de la base de datos y cada
# atributo de tipo models.* en una columna.

from django.db import models
# `models` trae la clase base (models.Model) y los tipos de campo
# (CharField, DateField, TimeField...) y utilidades como UniqueConstraint.


class Cita(models.Model):
    """Cita de la veterinaria, ahora persistida en SQLite mediante el ORM.

    En la Semana 2 `Cita` era una clase normal y los datos vivían en una lista
    en memoria. Al heredar de `models.Model`, Django la mapea a la tabla
    `vet_cita` y permite consultarla/guardarla con el ORM (`Cita.objects...`).
    """

    # --- Catálogos SERVICIOS y ESTADOS -----------------------------------
    # ¿Por qué viven en el código y no en una tabla?
    # Son catálogos CERRADOS: la veterinaria ofrece un conjunto fijo de 4
    # servicios y una cita solo puede estar en 3 estados. No los da de alta el
    # usuario, no cambian mientras el servidor corre y no tienen datos propios
    # (precio, duración, etc.), solo el nombre. Por eso NO se crea una tabla
    # aparte: se usan como `choices` del campo, que es lo que Django recomienda
    # para listas de opciones fijas. Django los aprovecha para validar el valor
    # guardado y para armar el desplegable del formulario.
    # Si algún día hubiera que administrarlos (agregar/quitar servicios,
    # ponerles precio), recién ahí se convertirían en un modelo `Servicio` con
    # relación `ForeignKey` hacia `Cita`.
    # Cada elemento es (valor_guardado_en_BD, texto_que_ve_el_usuario).
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

    # --- Campos = columnas de la tabla ----------------------------------
    # El primer argumento ('Mascota', 'Dueño'...) es el verbose_name: la
    # etiqueta legible que Django usa en formularios y en el admin.
    mascota = models.CharField('Mascota', max_length=100)   # texto corto
    dueno = models.CharField('Dueño', max_length=100)       # texto corto
    servicio = models.CharField('Servicio', max_length=20, choices=SERVICIOS)
    fecha = models.DateField('Fecha')                       # solo fecha
    hora = models.TimeField('Hora')                         # solo hora
    estado = models.CharField(
        'Estado', max_length=20, choices=ESTADOS, default='Pendiente',
    )  # `default`: si el formulario no lo manda, la cita nace 'Pendiente'.

    # --- class Meta -----------------------------------------------------
    # `Meta` va DENTRO de `Cita` (clase anidada) a propósito: es la forma en
    # que Django recibe la configuración del modelo SIN que esos valores se
    # confundan con columnas de la tabla. Si `ordering` o `constraints`
    # estuvieran sueltos como atributos de `Cita`, Django intentaría tratarlos
    # como campos. Al aislarlos en `Meta`, quedan como "opciones del modelo".
    class Meta:
        # Orden por defecto de cualquier consulta: primero por fecha, luego
        # por hora. Antes esto se hacía con sorted(...) en la View.
        ordering = ['fecha', 'hora']
        # Regla a nivel de BASE DE DATOS: no puede haber dos citas con la
        # misma fecha y hora. Antes solo lo revisaba el formulario; ahora lo
        # garantiza la propia tabla.
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'hora'], name='cita_horario_unico',
            ),
        ]

    # --- __str__ ------------------------------------------------------
    # Cómo se "ve" una Cita cuando se imprime: en el admin, en el shell y en
    # los mensajes. Sin esto, Django mostraría "Cita object (1)".
    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'
