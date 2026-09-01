# Informe — Laboratorio 03: Models, Django ORM y SQLite

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Lucas Inga - Renzo Leon

## Ejercicio 1 — Recuperar y analizar la aplicación anterior

**Entidad principal:** `Cita`, con los campos `mascota`, `dueno`, `servicio`,
`fecha`, `hora` y `estado`.

**Datos en memoria:** en la Semana 2, `Cita` era una clase Python común (no
heredaba de `models.Model`); la única fuente de datos era la lista `citas`
definida en `models.py`.

**Views/URLs/Forms/Templates:** `cita_list` (listado), `cita_crear`
(formulario `CitaForm` que hacía `citas.append(...)`), rutas
`vet:cita_list`/`vet:cita_crear`, templates `cita_list.html`/`cita_form.html`.

**Qué pasa al reiniciar el servidor:** la lista vive solo en la memoria del
proceso; al reiniciar el servidor, vuelve a sus 5 valores iniciales y
cualquier cita agregada durante la ejecución se pierde por completo.

## Ejercicio 2 — Convertir la entidad en un Django Model

Se reemplazó la clase Python común y la lista `citas` en memoria por un
**Django Model** real (`vet/models.py`). El modelo hereda de
`django.db.models.Model`, por lo que Django puede mapearlo a una tabla de
SQLite y operarlo mediante el ORM.

**Campos** (mismos que la Semana 2, con tipos de datos propios de Django):

| Campo | Tipo Django | Notas |
|-------|-------------|-------|
| `mascota` | `CharField(max_length=100)` | Texto corto |
| `dueno` | `CharField(max_length=100)` | Texto corto |
| `servicio` | `CharField(max_length=20, choices=SERVICIOS)` | Catálogo `Cita.SERVICIOS`: Consulta / Vacunación / Cirugía / Baño |
| `fecha` | `DateField` | Fecha de la cita |
| `hora` | `TimeField` | Hora de la cita |
| `estado` | `CharField(max_length=20, choices=ESTADOS, default='Pendiente')` | Catálogo `Cita.ESTADOS`: Pendiente / Confirmada / Atendida |

**Observación del profesor — por qué `SERVICIOS` y `ESTADOS` son código y no una
tabla.** El profesor pidió justificarlo con un comentario en el propio código
(hecho en `models.py`). El razonamiento:

- Son **catálogos cerrados**: 4 servicios y 3 estados fijos, definidos por la
  veterinaria.
- **No los administra el usuario** ni cambian mientras el servidor corre.
- **No tienen datos propios** (precio, duración…), solo el nombre.

Por eso se usan como `choices` del campo —la forma recomendada por Django para
listas de opciones fijas— y no como una tabla aparte, que solo añadiría un JOIN
en cada consulta sin aportar nada. Si en el futuro hubiera que gestionarlos
(agregar servicios, ponerles precio), recién ahí se convertirían en un modelo
`Servicio` con `ForeignKey` hacia `Cita`. También se eliminó una duplicación de
esas listas a nivel de módulo que había quedado sin uso.

**`class Meta`:**

- `ordering = ['fecha', 'hora']` — el listado sale ordenado por fecha y hora sin
  tener que ordenarlo en la View (antes se hacía con `sorted(...)`).
- `UniqueConstraint(fields=['fecha', 'hora'])` — la base de datos impide dos
  citas en el mismo horario (antes esa validación estaba solo en el formulario).

**`__str__`** se conserva igual, para que el registro se lea claro en el admin y
en el shell.

```python
class Cita(models.Model):
    # ¿Por qué SERVICIOS y ESTADOS viven en el código y no en una tabla?
    # Son catálogos cerrados (4 servicios, 3 estados), no los da de alta el
    # usuario, no cambian en ejecución y no tienen datos propios: por eso se
    # usan como `choices` del campo y no como una tabla aparte. Si hubiera que
    # administrarlos, se pasarían a un modelo `Servicio` con `ForeignKey`.
    SERVICIOS = [('Consulta', 'Consulta'), ('Vacunación', 'Vacunación'),
                 ('Cirugía', 'Cirugía'), ('Baño', 'Baño')]
    ESTADOS = [('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'),
               ('Atendida', 'Atendida')]

    mascota = models.CharField('Mascota', max_length=100)
    dueno = models.CharField('Dueño', max_length=100)
    servicio = models.CharField('Servicio', max_length=20, choices=SERVICIOS)
    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS,
                              default='Pendiente')

    class Meta:
        ordering = ['fecha', 'hora']
        constraints = [
            models.UniqueConstraint(fields=['fecha', 'hora'],
                                    name='cita_horario_unico'),
        ]

    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'
```

El formulario (`vet/forms.py`) toma sus opciones de `Cita.SERVICIOS` en vez de
tener otra copia de la lista.

> `views.py` todavía referencia la lista `citas` de la Semana 2, por lo que el
> servidor no arranca hasta rehacer la consulta (Ejercicio 4) y el registro
> (Ejercicio 5) con el ORM. La estructura de la tabla se crea en el Ejercicio 3.