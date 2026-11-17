# Exposición — Laboratorio 04, Parte 1: Relaciones entre Models en la app `vet`

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** agregar a la app `vet` los tres tipos de relación de Django —uno a
uno, uno a muchos y muchos a muchos con modelo intermedio—, migrarlos, y
consultarlos y mostrarlos de forma eficiente.

> Este documento explica, en el orden en que se hicieron, los pasos de la
> Parte 1 del Laboratorio 4. La Parte 2 (relaciones en `biblioteca`:
> `CarnetSocio` y `Prestamo`) corresponde a Lucas Inga.
>
> Nota: este laboratorio no tiene un `INFORME_Lab04.md` en el repositorio;
> esta exposición se armó a partir del código de `vet` y de los commits del
> Lab 04.

---

## Conceptos clave (lectura rápida)

- **Cardinalidad:** cuántos objetos de un lado se relacionan con cuántos del otro; **nace de las reglas del negocio**.
- **Uno a uno (1:1) → `OneToOneField`:** cada cita tiene **como máximo una** ficha clínica.
- **Uno a muchos (1:N) → `ForeignKey`:** un veterinario atiende **muchas** citas; la FK va en el lado **"muchos"** (`Cita`).
- **Muchos a muchos (N:M) → `ManyToManyField`:** una cita usa muchos insumos y un insumo se usa en muchas citas.
- **Modelo intermedio (`through`):** cuando la relación N:M **guarda datos propios** (cantidad, precio), se crea un modelo aparte: **`ConsumoInsumo`**.
- **`on_delete`:** qué pasa al borrar el objeto relacionado; es una **decisión de negocio**:
  - **`CASCADE`** → borra también los dependientes.
  - **`SET_NULL`** → deja el campo vacío (requiere `null=True`).
  - **`PROTECT`** → **impide** borrar si hay dependientes.
- **`related_name`:** nombre del **acceso inverso**: `veterinario.citas.all()`, `cita.ficha`.
- **Acceso directo / inverso:** directo = `cita.veterinario`; inverso = `veterinario.citas.all()`.
- **Problema N+1:** una consulta para la lista **+ una más por cada fila** al recorrer una relación.
- **`select_related`:** para relaciones **de a uno** (FK, 1:1); un **JOIN**, **una sola consulta**.
- **`prefetch_related`:** para relaciones **de a muchos** (N:M, FK inversa); **una consulta por relación**, unidas en Python.

---

## De dónde partimos

Después de la Semana 3, `vet` tenía **una sola tabla**: `Cita`, persistida
en SQLite con el ORM, con listado y registro funcionando. Pero una
veterinaria real no trabaja con datos sueltos: cada cita la atiende un
veterinario, algunas generan una ficha clínica y en cada atención se
consumen insumos.

La idea central de la semana es que **la cardinalidad sale de las reglas del
negocio**, y Django la representa con un tipo de campo:

| Relación | Campo de Django | En `vet` |
|---|---|---|
| 1:1 | `OneToOneField` | `FichaClinica` ↔ `Cita` |
| 1:N | `ForeignKey` | `Veterinario` → muchas `Cita` |
| N:M | `ManyToManyField` (+ `through`) | `Cita` ↔ `Insumo` vía `ConsumoInsumo` |

La relación se **define** en el Model, la View la **consulta** y el Template
la **presenta**.

---

## Paso 1 — Recuperar la aplicación (Ejercicio 1)

**Ver en el código:** [vet/models.py — `Cita` (L35)](django_project/src/vet/models.py#L35) · [vet/migrations/0001_initial.py (L14)](django_project/src/vet/migrations/0001_initial.py#L14)

Se partió de la app de la Semana 3: el modelo `Cita` con su migración
`0001_initial` aplicada, y las vistas `cita_list` y `cita_crear` leyendo y
escribiendo con el ORM. Las citas ya cargadas en la base se conservaron;
eso condicionó una decisión del Paso 3.

---

## Paso 2 — Relación uno a uno: `FichaClinica` (Ejercicio 2)

**Ver en el código:** [vet/models.py — `FichaClinica` (L86)](django_project/src/vet/models.py#L86) · [`OneToOneField` (L93)](django_project/src/vet/models.py#L93)

**Regla de negocio:** cuando una cita se atiende, se le abre una ficha
clínica; como máximo una por cita, y no toda cita la tiene.

```python
class FichaClinica(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE,
                                related_name='ficha')
    peso_kg = models.DecimalField('Peso (kg)', max_digits=5, decimal_places=2)
    diagnostico = models.TextField()
    tratamiento = models.TextField(blank=True)
    proximo_control = models.DateField(null=True, blank=True)
```

- `OneToOneField` garantiza que no haya dos fichas para la misma cita.
- `CASCADE`: una ficha sin su cita sería un dato huérfano, así que se borra
  junto con ella.
- `related_name='ficha'` permite el acceso inverso: `cita.ficha`.

---

## Paso 3 — Relación uno a muchos: `Veterinario` (Ejercicio 3)

**Ver en el código:** [vet/models.py — `Veterinario` (L9)](django_project/src/vet/models.py#L9) · [`ForeignKey` en `Cita` (L64)](django_project/src/vet/models.py#L64) · [`SET_NULL` (L66)](django_project/src/vet/models.py#L66)

**Regla de negocio:** un veterinario atiende muchas citas, pero cada cita la
atiende uno solo.

```python
class Veterinario(models.Model):
    nombre = models.CharField(max_length=100)
    colegiatura = models.CharField('N° de colegiatura', max_length=20, unique=True)
    especialidad = models.CharField(max_length=60, blank=True)

# dentro de Cita
veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='citas')
```

La `ForeignKey` va en `Cita` porque es el lado "muchos". Dos decisiones:

- **`SET_NULL`**: si un veterinario deja la clínica, su historial de citas
  **no** debe borrarse; la cita queda como "sin asignar".
- **`null=True`** era además obligatorio: la tabla ya tenía filas cuando se
  agregó la columna, y sin `null` Django habría pedido un valor por defecto
  para todas ellas.

---

## Paso 4 — Relación muchos a muchos con modelo intermedio (Ejercicio 4)

**Ver en el código:** [vet/models.py — `Insumo` (L19)](django_project/src/vet/models.py#L19) · [`ConsumoInsumo` (L111)](django_project/src/vet/models.py#L111) · [`subtotal` (L128)](django_project/src/vet/models.py#L128) · [`ManyToManyField` con `through` (L75)](django_project/src/vet/models.py#L75)

**Regla de negocio:** en una cita se usan varios insumos, y un insumo se usa
en muchas citas. Pero además importa **cuánto** se usó y **a qué precio** se
cobró ese día — datos que no son ni de la cita ni del insumo, sino de la
relación. Por eso no basta un `ManyToManyField` simple:

```python
class Insumo(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    unidad = models.CharField('Unidad de medida', max_length=20, default='unidad')
    stock = models.PositiveIntegerField(default=0)

class ConsumoInsumo(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='consumos')
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT, related_name='consumos')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=7, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

# dentro de Cita
insumos = models.ManyToManyField(Insumo, through='ConsumoInsumo',
                                 related_name='citas', blank=True)
```

- `through='ConsumoInsumo'` le dice a Django que la tabla intermedia es un
  modelo propio con sus campos.
- `CASCADE` desde la cita (si se borra la cita, sus consumos no tienen
  sentido) y `PROTECT` desde el insumo (no se puede borrar un insumo que ya
  figura en atenciones registradas).
- `subtotal` se calcula, no se guarda.

---

## Paso 5 — Migrar las relaciones (Ejercicio 5)

**Ver en el código:** [vet/migrations/0002_... (L14)](django_project/src/vet/migrations/0002_insumo_veterinario_fichaclinica_consumoinsumo_and_more.py#L14) · [`AddField` veterinario (L61)](django_project/src/vet/migrations/0002_insumo_veterinario_fichaclinica_consumoinsumo_and_more.py#L61) · [cargar_datos.py (L12)](django_project/src/cargar_datos.py#L12)

```powershell
python manage.py makemigrations vet
python manage.py migrate
```

Se generó `vet/migrations/0002_insumo_veterinario_fichaclinica_consumoinsumo_and_more.py`,
que crea las tablas `Veterinario`, `Insumo`, `FichaClinica` y
`ConsumoInsumo` y agrega la columna `veterinario` a `Cita`. Las citas que ya
existían se conservaron, con veterinario vacío gracias al `null=True`.

Para tener datos con los cuales probar se escribió `cargar_datos.py`, que
crea dos veterinarios, citas asignadas, una ficha clínica, tres insumos y
sus consumos:

```powershell
python manage.py shell < cargar_datos.py
```

---

## Paso 6 — Consultar las relaciones de forma eficiente (Ejercicio 6)

**Ver en el código:** [vet/views.py — `cita_list` con `select_related` (L18)](django_project/src/vet/views.py#L18) · [`cita_detalle` (L26)](django_project/src/vet/views.py#L26) · [`prefetch_related` (L33)](django_project/src/vet/views.py#L33) · [ruta `cita/<int:pk>/` (L17)](django_project/src/vet/urls.py#L17)

Se agregó la vista `cita_detalle` y la ruta `cita/<int:pk>/`, y se ajustó el
listado:

```python
def cita_list(request):
    citas = (Cita.objects
             .select_related('veterinario', 'ficha')
             .order_by('fecha', 'hora'))
    ...

def cita_detalle(request, pk):
    cita = get_object_or_404(
        Cita.objects
            .select_related('veterinario', 'ficha')
            .prefetch_related('consumos__insumo'),
        pk=pk,
    )
    total = sum(c.subtotal for c in cita.consumos.all())
```

- **`select_related`** para las relaciones "de a uno" (la FK al veterinario
  y el 1:1 de la ficha): resuelve todo con un JOIN en **una sola consulta**,
  en vez de una consulta extra por cada fila del listado.
- **`prefetch_related('consumos__insumo')`** para la relación "de a muchos":
  hace una consulta para los consumos y otra para los insumos, y Django los
  une en Python.
- `get_object_or_404` devuelve una página 404 si la cita no existe.

---

## Paso 7 — Mostrar las relaciones en los templates (Ejercicio 7)

**Ver en el código:** [templates/vet/cita_detalle.html — acceso directo (L12)](django_project/src/templates/vet/cita_detalle.html#L12) · [acceso inverso (L16)](django_project/src/templates/vet/cita_detalle.html#L16) · [modelo intermedio (L29)](django_project/src/templates/vet/cita_detalle.html#L29) · [cita_list.html — columna Veterinario (L38)](django_project/src/templates/vet/cita_list.html#L38)

`cita_detalle.html` muestra las tres formas de recorrer una relación, cada
una marcada con un comentario:

1. **Acceso directo a la FK (1:N):** `{{ cita.veterinario.nombre }}`.
2. **Acceso inverso al 1:1:** `{% if cita.ficha %}` … `{{ cita.ficha.diagnostico }}`,
   con un mensaje si la cita aún no fue atendida.
3. **Recorrido del modelo intermedio:** `{% for consumo in cita.consumos.all %}`,
   mostrando `consumo.insumo.nombre`, la cantidad, el precio y el subtotal,
   y al final el total en insumos.

En el listado se agregó la columna **Veterinario** (con "Sin asignar" si no
hay) y un enlace **Ver detalle** en cada fila.

---

## Qué mostrar para verificar cada paso

> No hay un informe del Lab 04 con resultados registrados; estas son las
> comprobaciones que conviene hacer en vivo durante la exposición.

| Paso | Qué comprobar |
|---|---|
| 5 | `showmigrations vet` muestra `0001` y `0002` aplicadas |
| 5 | Las citas anteriores siguen en el listado, con veterinario vacío |
| 6 | El listado muestra la columna Veterinario ("Sin asignar" si no hay) |
| 6 | `/cita/<pk>/` de una cita inexistente devuelve 404 |
| 7 | El detalle de Rocky muestra veterinario, ficha y 3 insumos con su total |
| 7 | El detalle de una cita sin ficha muestra el aviso "aún no tiene ficha" |

---

## Conclusión de la Parte 1

El hilo conductor es que **cada relación es una decisión de negocio, no solo
técnica**: qué lado lleva la FK, qué pasa al borrar (`CASCADE`, `SET_NULL`,
`PROTECT`) y si la relación guarda datos propios (y por eso necesita un
modelo intermedio). Una vez definidas en el Model, la vista las consulta sin
multiplicar consultas (`select_related` / `prefetch_related`) y el template
las recorre en ambos sentidos gracias a `related_name`. Estas tres
relaciones son exactamente las que la Semana 5 expone en el Django Admin
sin tocar `models.py`.
