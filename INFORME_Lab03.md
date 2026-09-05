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

Los archivos de la App (`models.py`, `forms.py`, `urls.py`, `apps.py`) llevan
**comentarios bloque por bloque** que explican para qué está cada parte — por
ejemplo, por qué `class Meta` va anidada dentro de `Cita`, o por qué el
formulario hereda de `forms.Form` y no de `ModelForm`.

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

### Ajuste posterior: simplificación al temario de la Semana 3

Al revisar el código contra el PPT de la semana se quitaron elementos que no
forman parte de lo enseñado, para que la App use únicamente lo visto en clase:

| Se quitó | Motivo | Reemplazo |
|----------|--------|-----------|
| `class Meta` con `ordering` y `UniqueConstraint` | No aparece en el material | El orden se hace en la View con `order_by()` |
| `.exists()` en el formulario | No aparece en el material | `Cita.objects.filter(...)`, que sí se enseña |
| `django.contrib.messages` | No aparece en el material | Basta el patrón Post/Redirect/Get |
| `verbose_name` posicional en cada campo | El modelo del PPT declara los campos sin él | `models.CharField(max_length=100)` |

Se mantiene `forms.Form` y **no** se usa `ModelForm`, tal como indica el
material de la semana.

## Ejercicio 3 — Crear la estructura persistente de datos

Hasta aquí `Cita` era solo una clase en Python: la tabla todavía no existía en
la base de datos. Las migraciones son el mecanismo con el que Django lleva lo
que está escrito en el modelo hacia la estructura real de SQLite. Primero se
genera el archivo de migración, que describe el cambio, y después se aplica
sobre la base. Es importante distinguir esto de las operaciones CRUD: las
migraciones cambian la **estructura**, el CRUD cambia los **datos**.

**Comandos ejecutados:**

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate vet 0001
```

**Capturas:**

- `ej3_makemigrations.png` — genera `vet/migrations/0001_initial.py` con la
  operación `Create model Cita`.
- `ej3_migrate.png` — aplica las migraciones; la última línea es
  `Applying vet.0001_initial... OK`.
- `ej3_showmigrations.png` — estado de todas las migraciones; `vet` aparece con
  `[X] 0001_initial`, es decir, aplicada.
- `ej3_sqlmigrate.png` — SQL que Django generó para esa migración.

**Migración generada** (`vet/migrations/0001_initial.py`): una sola operación
`CreateModel` con los seis campos del modelo más el `id` que Django agrega
automáticamente como clave primaria.

**SQL que produce la migración** (visto con `sqlmigrate`, no se escribió a mano):

```sql
CREATE TABLE "vet_cita" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "mascota" varchar(100) NOT NULL,
    "dueno" varchar(100) NOT NULL,
    "servicio" varchar(20) NOT NULL,
    "fecha" date NOT NULL,
    "hora" time NOT NULL,
    "estado" varchar(20) NOT NULL
);
```

El archivo `db.sqlite3` queda creado en `django_project/src/` y contiene la
tabla `vet_cita` junto a las tablas internas de Django. No se sube al
repositorio porque está en `.gitignore`: cualquiera que clone el proyecto la
regenera con `migrate`.

**Casos de prueba:**

| # | Caso | Resultado esperado | Resultado obtenido |
|---|------|--------------------|--------------------|
| 1 | `makemigrations` con el modelo `Cita` recién creado | Genera `0001_initial.py` con `Create model Cita` | Correcto |
| 2 | `migrate` sobre una base vacía | Aplica todas las migraciones, incluida `vet.0001_initial` | Correcto |
| 3 | `showmigrations` después de migrar | `vet` muestra `[X] 0001_initial` | Correcto |
| 4 | `makemigrations` una segunda vez sin tocar el modelo | No detecta cambios | Correcto |
| 5 | `sqlmigrate vet 0001` | Muestra el `CREATE TABLE` de `vet_cita` | Correcto |

## Ejercicio 4 — Implementar la consulta mediante ORM

La vista del listado dejó de recorrer una lista de Python y ahora le pide los
datos a la base. El punto de entrada es el Manager `objects` del modelo, que
devuelve un QuerySet; el ORM traduce ese QuerySet a una consulta SELECT y
SQLite responde con los registros guardados. El template no cambió en nada:
sigue recorriendo una colección de citas, solo que ahora vienen del disco y no
de la memoria del proceso.

**Antes (Semana 2) y ahora (Semana 3):**

```python
# Semana 2 — lista en memoria
citas_ordenadas = sorted(citas, key=lambda c: (c.fecha, c.hora))

# Semana 3 — consulta con el ORM
citas = Cita.objects.order_by('fecha', 'hora')
```

**Vista final** (`vet/views.py`):

```python
def cita_list(request):
    citas = Cita.objects.order_by('fecha', 'hora')
    return render(request, 'vet/cita_list.html', {'citas': citas})
```

**Recorrido de la consulta:**

```
GET / → config/urls.py → vet/urls.py → cita_list()
      → Cita.objects.order_by('fecha','hora') → QuerySet → Django ORM
      → SELECT → SQLite → Context → cita_list.html → Response
```

Los cinco registros de ejemplo de la Semana 2 se cargaron una sola vez desde el
shell de Django con `Cita.objects.create(...)`, de modo que ya viven en la
tabla y no en el código.

**Capturas:**

- `ej4_orm_shell.png` — el QuerySet consultado desde el shell: cinco objetos
  `Cita` traídos de SQLite y el conteo total.
- `ej4_listado.png` — el mismo listado en el navegador, servido desde la base
  de datos.

**Casos de prueba:**

| # | Caso | Resultado esperado | Resultado obtenido |
|---|------|--------------------|--------------------|
| 1 | Abrir la página principal | Responde 200 y muestra las cinco citas de la tabla | Correcto |
| 2 | Orden de las filas | De la cita más próxima a la más lejana, por fecha y hora | Correcto |
| 3 | Consultar el QuerySet desde el shell | Devuelve los mismos cinco registros que el navegador | Correcto |
| 4 | Conteo de registros | `count()` devuelve 5 | Correcto |
| 5 | Reiniciar el servidor y volver a abrir el listado | Las cinco citas siguen ahí | Correcto |
| 6 | Template sin modificar | Muestra los datos igual que en la Semana 2 | Correcto |