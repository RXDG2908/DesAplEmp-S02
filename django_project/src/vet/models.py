# vet/models.py
# Aquí se define la capa de DATOS de la App (la "M" de MVT). Cada clase que
# hereda de models.Model se convierte en una tabla de la base de datos y cada
# atributo de tipo models.* en una columna.

from django.db import models
# `models` trae la clase base (models.Model) y los tipos de campo
# (CharField, DateField, TimeField...).


class Cita(models.Model):
    """Cita de la veterinaria, ahora persistida en SQLite mediante el ORM.

    En la Semana 2 `Cita` era una clase normal y los datos vivían en una lista
    en memoria. Al heredar de `models.Model`, Django la mapea a la tabla
    `vet_cita` y permite consultarla/guardarla con el ORM (`Cita.objects...`).
    Django agrega solo el campo `id` como clave primaria.
    """

    # --- Catálogos SERVICIOS y ESTADOS -----------------------------------
    # ¿Por qué viven en el código y no en una tabla?
    # Son catálogos CERRADOS: la veterinaria ofrece un conjunto fijo de 4
    # servicios y una cita solo puede estar en 3 estados. No los da de alta el
    # usuario, no cambian mientras el servidor corre y no tienen datos propios
    # (precio, duración, etc.), solo el nombre. Por eso NO se crea una tabla
    # aparte: se usan como `choices` del campo.
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
    mascota = models.CharField(max_length=100)
    dueno = models.CharField(max_length=100)
    servicio = models.CharField(max_length=20, choices=SERVICIOS)
    fecha = models.DateField()
    hora = models.TimeField()
    # `default`: si el formulario no lo manda, la cita nace 'Pendiente'.
    estado = models.CharField(max_length=20, choices=ESTADOS,
                              default='Pendiente')

    # Cómo se "ve" una Cita cuando se imprime en el shell o en el admin.
    # Sin esto, Django mostraría "Cita object (1)".
    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'
