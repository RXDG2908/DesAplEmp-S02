# Exposición — Laboratorio 03, Parte 1: de la lista en memoria a Django ORM y SQLite (app `vet`)

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** migrar la app `vet` de la Semana 2 para que sus citas se guarden
en una base de datos SQLite real, usando un Django Model, migraciones y el
ORM.

> Este documento explica, en el orden en que se hicieron, los seis
> ejercicios de la Parte 1 del Laboratorio 3. La Parte 2 (app `biblioteca`)
> corresponde a Lucas Inga.

---

## Conceptos clave (lectura rápida)

- **Django Model:** clase que hereda de **`models.Model`**; cada clase es una **tabla** y cada atributo una **columna**.
- **ORM (Object-Relational Mapping):** traduce operaciones con **objetos Python** a **SQL**, sin escribir SQL a mano.
- **Manager (`objects`):** la puerta de entrada al ORM: `Cita.objects`.
- **QuerySet:** el resultado de una consulta (`Cita.objects.order_by(...)`); es **perezoso**: no va a la base hasta que se usa.
- **`choices`:** lista **cerrada** de opciones para un campo (`SERVICIOS`, `ESTADOS`); se usa cuando las opciones **no cambian** y **no tienen datos propios**.
- **Migración:** archivo que registra, de forma **versionada**, los cambios del Model.
  - **`makemigrations`** → **crea** el archivo de migración.
  - **`migrate`** → lo **aplica** a la base de datos.
- **Migraciones vs. CRUD:** las migraciones cambian la **estructura**; el CRUD cambia los **datos**.
- **CRUD:** **C**reate (`create`), **R**ead (`all`, `filter`, `order_by`), **U**pdate, **D**elete.
- **SQLite:** la base de datos en un **archivo** (`db.sqlite3`); no se sube al repositorio, se **regenera con `migrate`**.
- **Persistencia:** los datos **sobreviven al reinicio** del servidor (lo que faltaba en la Semana 2).

---

> **Enlaces al código:** abren el archivo actual en la línea exacta. El
> código ya incluye agregados de semanas posteriores (relaciones,
> QuerySet propio), pero las líneas enlazadas son las de este laboratorio.

---

## De dónde partimos

Al terminar la Semana 2, la app `vet` funcionaba de punta a punta —listado,
formulario, validación de horario— pero con un problema de fondo: las citas
vivían en una lista de Python dentro de `models.py`. Cualquier cita
registrada desaparecía al reiniciar el servidor.

La idea central de este laboratorio es que **la persistencia se agrega sin
rehacer la aplicación**: se cambia lo que hay detrás del "Model", y la
vista solo cambia la forma de pedir y guardar los datos. El template, por
ejemplo, no se toca.

---

## Paso 1 — Recuperar y analizar la aplicación anterior (Ejercicio 1)

**Ver en el código:** [vet/models.py (L35)](django_project/src/vet/models.py#L35) · [vet/views.py (L14)](django_project/src/vet/views.py#L14) · [vet/urls.py (L14)](django_project/src/vet/urls.py#L14) · [vet/forms.py (L9)](django_project/src/vet/forms.py#L9)

Antes de cambiar nada se hizo el inventario de lo que había:

- **Entidad:** `Cita` (mascota, dueño, servicio, fecha, hora, estado), como
  clase Python común que no heredaba de `models.Model`.
- **Datos:** la lista `citas` en `models.py`, única fuente de datos.
- **Vistas y rutas:** `cita_list` y `cita_crear`, con las rutas
  `vet:cita_list` y `vet:cita_crear`.
- **Formulario y plantillas:** `CitaForm`, que hacía `citas.append(...)`, y
  las plantillas `cita_list.html` y `cita_form.html`.

Y la respuesta a la pregunta clave: al reiniciar el servidor, la lista
vuelve a sus 5 valores iniciales y todo lo agregado se pierde.

---

## Paso 2 — Convertir la entidad en un Django Model (Ejercicio 2)

**Ver en el código:** [vet/models.py — `class Cita(models.Model)` (L35)](django_project/src/vet/models.py#L35) · [`SERVICIOS` (L37)](django_project/src/vet/models.py#L37) · [`ESTADOS` (L43)](django_project/src/vet/models.py#L43) · [campos (L49)](django_project/src/vet/models.py#L49) · [vet/forms.py — `choices=Cita.SERVICIOS` (L15)](django_project/src/vet/forms.py#L15)

Se reemplazó la clase común y la lista por un Model real:

```python
class Cita(models.Model):
    SERVICIOS = [('Consulta', 'Consulta'), ('Vacunación', 'Vacunación'),
                 ('Cirugía', 'Cirugía'), ('Baño', 'Baño')]
    ESTADOS = [('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'),
               ('Atendida', 'Atendida')]

    mascota = models.CharField(max_length=100)
    dueno = models.CharField(max_length=100)
    servicio = models.CharField(max_length=20, choices=SERVICIOS)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
```

Al heredar de `models.Model`, Django ya puede mapear la clase a una tabla y
operarla con el ORM. Los campos son los mismos de la Semana 2, ahora con
tipos de Django.

**Observación del profesor: ¿por qué `SERVICIOS` y `ESTADOS` están en el
código y no en una tabla?** Se respondió con un comentario en el propio
`models.py`: son catálogos **cerrados** (4 servicios, 3 estados), no los
administra el usuario, no cambian mientras el sistema corre y no tienen
datos propios como precio o duración. Por eso van como `choices`. Si algún
día hubiera que administrarlos, recién ahí pasarían a ser un modelo
`Servicio` con una `ForeignKey`.

Después se hizo un **ajuste al temario**: se quitaron elementos que no se
vieron en clase (`class Meta` con `ordering` y `UniqueConstraint`,
`.exists()`, `messages`, `verbose_name`). El orden pasó a hacerse en la
vista con `order_by()`, y se mantuvo `forms.Form` en lugar de `ModelForm`,
como indica el material.

---

## Paso 3 — Crear la estructura persistente (Ejercicio 3)

**Ver en el código:** [vet/migrations/0001_initial.py — `CreateModel` (L14)](django_project/src/vet/migrations/0001_initial.py#L14)

Hasta aquí `Cita` era solo código: la tabla no existía. Para crearla se
usaron las migraciones:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate vet 0001
```

`makemigrations` generó `vet/migrations/0001_initial.py` con la operación
`Create model Cita`; `migrate` la aplicó (`Applying vet.0001_initial... OK`);
`showmigrations` la mostró marcada con `[X]`; y `sqlmigrate` dejó ver el SQL
que Django escribió solo:

```sql
CREATE TABLE "vet_cita" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "mascota" varchar(100) NOT NULL,
    ...
    "estado" varchar(20) NOT NULL
);
```

La distinción que se remarca aquí: **las migraciones cambian la estructura;
el CRUD cambia los datos.** El `db.sqlite3` no se sube al repositorio (está
en `.gitignore`); quien clone el proyecto lo regenera con `migrate`.

---

## Paso 4 — La consulta mediante el ORM (Ejercicio 4)

**Ver en el código:** [vet/views.py — `cita_list` (L14)](django_project/src/vet/views.py#L14) · [`order_by` (L19)](django_project/src/vet/views.py#L19) · [templates/vet/cita_list.html (L28)](django_project/src/templates/vet/cita_list.html#L28)

La vista del listado dejó de recorrer una lista y pasó a pedirle los datos a
la base:

```python
# Semana 2 — lista en memoria
citas_ordenadas = sorted(citas, key=lambda c: (c.fecha, c.hora))

# Semana 3 — consulta con el ORM
citas = Cita.objects.order_by('fecha', 'hora')
```

`Cita.objects` es el Manager; devuelve un QuerySet que el ORM traduce a un
`SELECT ... ORDER BY fecha, hora`. Las cinco citas de ejemplo se cargaron una
sola vez desde el shell con `Cita.objects.create(...)`, así que ya viven en
la tabla y no en el código.

El template **no cambió nada**: sigue recibiendo una colección de citas,
solo que ahora vienen del disco. Y la prueba que importa: al reiniciar el
servidor, las cinco citas siguen ahí.

---

## Paso 5 — El registro mediante el ORM (Ejercicio 5)

**Ver en el código:** [vet/views.py — `cita_crear` (L41)](django_project/src/vet/views.py#L41) · [`Cita.objects.create` (L47)](django_project/src/vet/views.py#L47) · [redirect (L54)](django_project/src/vet/views.py#L54) · [vet/forms.py — `filter` en `clean()` (L33)](django_project/src/vet/forms.py#L33)

`CitaForm` mantuvo su validación; lo que cambió fue qué hace la vista
cuando el formulario es válido: en lugar de `citas.append(...)` llama a
`Cita.objects.create(...)`, que el ORM convierte en un `INSERT` sobre
`vet_cita`.

La validación de horario también pasó a consultar la base: el `clean()` del
formulario usa `Cita.objects.filter(fecha=fecha, hora=hora)`, y si encuentra
algo rechaza la cita.

Tras un POST válido se redirige a `vet:cita_list` (**Post/Redirect/Get**), y
el listado vuelve a consultar la base, ya con la cita nueva. Refrescar la
página no duplica el registro.

---

## Paso 6 — Analizar el flujo de persistencia (Ejercicio 6)

**Ver en el código:** [config/urls.py (L22)](django_project/src/config/urls.py#L22) · [vet/urls.py (L14)](django_project/src/vet/urls.py#L14) · [vet/views.py (L14)](django_project/src/vet/views.py#L14)

```
GET / → config/urls.py → vet/urls.py → cita_list()
      → Cita.objects.order_by('fecha','hora') → QuerySet → Django ORM
      → SELECT → SQLite → Context → cita_list.html → Response
```

| Operación Django ORM | SQL conceptual |
|---|---|
| `Cita.objects.order_by('fecha','hora')` | `SELECT * FROM vet_cita ORDER BY fecha, hora` |
| `Cita.objects.create(**datos)` | `INSERT INTO vet_cita (...) VALUES (...)` |
| `Cita.objects.filter(fecha=..., hora=...)` | `SELECT * FROM vet_cita WHERE fecha=? AND hora=?` |

El navegador nunca habla con SQLite: siempre pasa por URL → View → Model →
ORM, y el ORM es el único que escribe SQL.

---

## Cómo se verificó cada paso (resumen de pruebas)

| Paso | Qué se probó | Resultado |
|---|---|---|
| 3 | `makemigrations` genera `0001_initial` y `migrate` la aplica | Correcto |
| 3 | `makemigrations` por segunda vez no detecta cambios | Correcto |
| 3 | `sqlmigrate vet 0001` muestra el `CREATE TABLE` | Correcto |
| 4 | El listado muestra las cinco citas desde la base, ordenadas | Correcto |
| 4 | `count()` devuelve 5 en el shell | Correcto |
| 4 | Reiniciar el servidor: las citas siguen ahí | Correcto |
| 5 | Una cita válida redirige (302) y aparece en el listado | Correcto |
| 5 | Una cita en un horario ocupado es rechazada | Correcto |
| 5 | Refrescar tras el redirect no duplica el registro | Correcto |

---

## Conclusión de la Parte 1

El hilo conductor es que **se cambió el origen de los datos sin cambiar la
forma de la aplicación**: el Model pasó de lista a tabla, la vista pasó de
`sorted`/`append` a `order_by`/`create`, y el template quedó idéntico. Las
migraciones crearon la estructura una sola vez, y desde ahí todas las
operaciones sobre los datos pasan por el ORM. Con eso desaparece el problema
de la Semana 2: las citas ya sobreviven a un reinicio del servidor.
