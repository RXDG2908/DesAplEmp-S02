# Exposición — Laboratorio 07, Parte 1: ORM avanzado sobre la app `vet`

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** usar las relaciones ya construidas en `vet` para registrar una
operación de forma segura (transacción + `F()`), generar reportes
(`aggregate` / `annotate`), encapsular reglas de negocio en un QuerySet
propio y medir y corregir el problema N+1.

> Este documento explica, en el orden en que se hicieron, los ocho
> ejercicios de la Parte 1 del Laboratorio 7. La Parte 2 (app `biblioteca`)
> corresponde a Lucas Inga.

---

## Conceptos clave (lectura rápida)

- **Transacción (`transaction.atomic()`):** un bloque **todo o nada**: si algo falla, se **deshacen** todas las operaciones de adentro. Evita **datos a medias**.
- **Expresión `F()`:** hace referencia al **valor de un campo en la base**; `F('stock') - 2` resta **dentro de la base de datos**, evitando que dos operaciones simultáneas **se pisen**.
- **`update()`:** modifica filas **directamente en la base** y devuelve **cuántas filas** cambió.
- **`aggregate()`:** **resume toda la tabla** en un valor; devuelve un **diccionario**, no un QuerySet (ej. **total global**).
- **`annotate()`:** agrega un **valor calculado a cada objeto**; sigue siendo un **QuerySet** (ej. **consumos por cita**).
- **`values()` + `annotate()`:** **agrupa** (ej. **citas por estado**), como un `GROUP BY`.
- **`Sum`, `Count`:** funciones de agregación.
- **QuerySet personalizado:** clase propia (`CitaQuerySet`) con métodos que son **reglas del negocio** (`con_estado`, `proximas`); son **encadenables**.
- **`as_manager()`:** convierte ese QuerySet en el **manager** `objects` del modelo.
- **Idempotente:** un script que se puede ejecutar **varias veces sin duplicar** datos (`get_or_create`).
- **Problema N+1:** **1 consulta** para la lista **+ N consultas** más, una por fila. Se mide con **`connection.queries`**.
  - **`select_related`** → relaciones **de a uno** (JOIN).
  - **`prefetch_related`** → relaciones **de a muchos** (consulta aparte, unión en Python).

---

## De dónde partimos

Para la Semana 7, `vet` ya tenía todo lo necesario: la cita con sus tres
relaciones (ficha 1:1, veterinario 1:N, insumos N:M a través de
`ConsumoInsumo`), el Admin configurado y los templates refactorizados.

La idea central del laboratorio es que **no se agregan entidades nuevas**:
se le saca más provecho al ORM sobre lo que ya existe. Operaciones que
tocan varias tablas a la vez sin dejar datos a medias, totales calculados
por la base de datos, reglas del negocio escritas una sola vez, y contar
cuántas consultas hace realmente cada pantalla.

---

## Paso 1 — Ubicar los campos clave (Ejercicio 1)

**Ver en el código:** [vet/models.py — `Insumo.stock` (L19)](django_project/src/vet/models.py#L19) · [`Cita.estado` (L54)](django_project/src/vet/models.py#L54) · [`ConsumoInsumo.cantidad` (L121)](django_project/src/vet/models.py#L121)

El laboratorio necesita tres tipos de campo, y los tres ya existían:

- **Un entero que se descuenta:** `Insumo.stock`.
- **Un campo de estado:** `Cita.estado` (Pendiente, Confirmada, Atendida).
- **Un atributo numérico del modelo intermedio:** `ConsumoInsumo.cantidad`,
  junto con `precio_unitario`.

Por eso no hizo falta ninguna migración nueva; se comprobó que
`makemigrations` no detectaba cambios.

---

## Paso 2 — Cargar datos de prueba (Ejercicio 2)

**Ver en el código:** [cargar_lab07.py (L9)](django_project/src/cargar_lab07.py#L9)

Se escribió `cargar_lab07.py`, un script **idempotente**: usa
`get_or_create`, así que se puede ejecutar varias veces sin duplicar nada.

```powershell
python manage.py shell -c "exec(open('cargar_lab07.py', encoding='utf-8').read())"
```

La base quedó con **5 citas** (en los tres estados), **3 veterinarios**,
**4 insumos** y **8 consumos**, cumpliendo el mínimo de la guía. Las citas
de Luna y Toby se dejaron con fecha de fines de octubre para que el reporte
tenga citas próximas.

---

## Paso 3 — Registrar una operación con transacción y `F()` (Ejercicio 3)

**Ver en el código:** [vet/views.py — `consumo_registrar` (L59)](django_project/src/vet/views.py#L59) · [`transaction.atomic` (L66)](django_project/src/vet/views.py#L66) · [`F()` y `stock__gte` (L76)](django_project/src/vet/views.py#L76) · [error (L78)](django_project/src/vet/views.py#L78) · [vet/forms.py — `ConsumoForm` (L41)](django_project/src/vet/forms.py#L41) · [ruta (L18)](django_project/src/vet/urls.py#L18) · [consumo_form.html (L8)](django_project/src/templates/vet/consumo_form.html#L8)

Se creó la pantalla "Registrar consumo de insumo" (ruta `consumo/nuevo/`,
vista `consumo_registrar`, formulario `ConsumoForm` y plantilla
`consumo_form.html`). Al enviar el formulario, la vista hace **tres cosas
dentro de un solo bloque transaccional**:

```python
with transaction.atomic():
    ConsumoInsumo.objects.create(cita=..., insumo=..., cantidad=..., precio_unitario=...)
    Cita.objects.filter(pk=cita.pk).update(estado='Atendida')
    filas = Insumo.objects.filter(
        pk=insumo.pk, stock__gte=cantidad,
    ).update(stock=F('stock') - cantidad)
    if filas == 0:
        raise ValueError('Stock insuficiente de ' + insumo.nombre)
```

- **`transaction.atomic()`**: o se guardan las tres operaciones, o ninguna.
  Si se lanza el error, todo lo de adentro se deshace.
- **`F('stock') - cantidad`**: la resta se hace **dentro de la base de
  datos**, no en Python. Así, si dos personas registran un consumo a la vez,
  no se pisa un descuento con el otro.
- **`stock__gte=cantidad`**: el descuento solo se aplica si alcanza; si no,
  `update` devuelve 0 filas, y eso dispara el error.
- Si sale bien, se redirige al detalle de la cita (**Post/Redirect/Get**); si
  falla, la plantilla muestra el mensaje.

**Las dos pruebas, con la jeringa de 5 ml (stock inicial 100):**

| Caso | Resultado |
|---|---|
| Toby, cantidad 2 | Redirige al detalle; Toby queda *Atendida*; consumos 8 → 9; stock 100 → 98 |
| Luna, cantidad 9999 | Mensaje "Stock insuficiente de Jeringa 5ml"; sigue habiendo 9 consumos y 98 jeringas, y Luna sigue *Pendiente* |

El segundo caso es el importante: el consumo que se había creado primero y
el cambio de estado **también se deshicieron**. Ningún registro quedó a
medias.

---

## Paso 4 — Un total con `aggregate()` (Ejercicio 4)

**Ver en el código:** [vet/views.py — `aggregate` (L89)](django_project/src/vet/views.py#L89)

En el shell se calculó el total consumido, sumando cantidad × precio de
todos los consumos:

```python
ConsumoInsumo.objects.aggregate(
    total=Sum(F('cantidad') * F('precio_unitario'), output_field=DecimalField())
)
# {'total': Decimal('110.50')}
```

`aggregate()` **no devuelve un QuerySet** sino un diccionario: resume toda
la tabla en un solo valor, que no es un objeto del modelo. Por eso es una
consulta final; no se le puede encadenar `filter()` ni `order_by()`.

---

## Paso 5 — Valores por objeto con `annotate()` (Ejercicio 5)

**Ver en el código:** [vet/views.py — `annotate` por cita (L92)](django_project/src/vet/views.py#L92) · [por estado (L93)](django_project/src/vet/views.py#L93)

```python
Cita.objects.annotate(n=Count('consumos')).order_by('-n')
# Rocky 3, Luna 2, Toby 2, Michi 1, Nala 1

Cita.objects.values('estado').annotate(total=Count('id')).order_by('-total')
# Atendida 3, Pendiente 1, Confirmada 1
```

A diferencia de `aggregate()`, aquí el resultado **sigue siendo un
QuerySet**: cada cita trae un valor calculado extra. Combinado con
`values('estado')`, `annotate` agrupa: una fila por estado con su conteo.

---

## Paso 6 — La página de reporte (Ejercicio 6)

**Ver en el código:** [vet/views.py — `reporte` (L88)](django_project/src/vet/views.py#L88) · [ruta `reporte/` (L19)](django_project/src/vet/urls.py#L19) · [templates/vet/reporte.html (L1)](django_project/src/templates/vet/reporte.html#L1)

Se creó la ruta `reporte/`, la vista `reporte` y la plantilla `reporte.html`
(que hereda de `base.html`). Muestra cuatro cosas:

- el total global consumido: **S/ 110.50**, con `floatformat:2`;
- el número de consumos por cita;
- las citas por estado;
- las citas próximas pendientes: **1** (la de Luna).

---

## Paso 7 — Un QuerySet personalizado (Ejercicio 7)

**Ver en el código:** [vet/models.py — `CitaQuerySet` (L28)](django_project/src/vet/models.py#L28) · [`as_manager()` (L55)](django_project/src/vet/models.py#L55) · [uso en `cita_list` (L20)](django_project/src/vet/views.py#L20) · [uso en `reporte` (L94)](django_project/src/vet/views.py#L94)

En `vet/models.py` se creó `CitaQuerySet` con dos métodos que representan
reglas del negocio, y se asignó como manager de `Cita`:

```python
class CitaQuerySet(models.QuerySet):
    def con_estado(self, estado):
        return self.filter(estado=estado)

    def proximas(self):
        return self.filter(fecha__gte=timezone.localdate())

class Cita(models.Model):
    ...
    objects = CitaQuerySet.as_manager()
```

Como devuelven QuerySets, **se pueden encadenar**. Se usan en dos vistas:

- `cita_list` filtra por estado con `citas.con_estado(estado)` cuando llega
  `?estado=` en la URL;
- `reporte` cuenta `Cita.objects.proximas().con_estado('Pendiente').count()`.

Se comprobó que el listado, el detalle y el filtro siguen respondiendo
normalmente: el CRUD de semanas anteriores no se rompió.

---

## Paso 8 — Medir y optimizar el problema N+1 (Ejercicio 8)

**Ver en el código:** [medir_n1.py (L1)](django_project/src/medir_n1.py#L1) · [vet/views.py — `select_related` (L18)](django_project/src/vet/views.py#L18) · [`prefetch_related` (L33)](django_project/src/vet/views.py#L33)

Con `DEBUG` activo se contaron las consultas con `connection.queries`,
reiniciando el contador con `reset_queries()` antes de cada medición (script
`medir_n1.py`). Con las 5 citas y 9 consumos:

| Pantalla | Sin optimizar | Optimizada |
|---|---|---|
| Citas con su veterinario | 6 consultas | **1** (`select_related`) |
| Citas con sus consumos e insumos | 15 consultas | **3** (`prefetch_related`) |

Sin optimizar, Django hace 1 consulta para las citas y luego **una más por
cada cita** para llegar al veterinario (6 = 1 + 5), y todavía una más por
cada consumo para llegar al insumo (15 = 1 + 5 + 9). Ese es el problema N+1:
las consultas crecen con las filas.

- **`select_related()`** → relaciones "de a uno" (FK, 1:1): un JOIN, una sola
  consulta.
- **`prefetch_related()`** → relaciones "de a muchos" (N:M, FK inversa): una
  consulta por relación, unidas en Python, porque un JOIN repetiría filas.

En la aplicación, el listado usa `select_related` para veterinario y ficha,
y el detalle usa `prefetch_related('consumos__insumo')`.

---

## Cómo se verificó cada paso (resumen de pruebas)

| Paso | Qué se probó | Resultado |
|---|---|---|
| 1 | `makemigrations` no detecta cambios | Correcto |
| 2 | Ejecutar `cargar_lab07.py` dos veces no duplica datos | Correcto |
| 3 | Consumo válido: guarda, marca Atendida y descuenta stock | Correcto |
| 3 | Stock insuficiente: muestra el error y no guarda nada | Correcto |
| 4 | `aggregate` devuelve `{'total': 110.50}` | Correcto |
| 5 | `annotate` da los consumos por cita y las citas por estado | Correcto |
| 6 | `/reporte/` muestra total, conteos y 1 cita próxima pendiente | Correcto |
| 7 | `?estado=Pendiente` filtra el listado con `con_estado` | Correcto |
| 8 | 6 → 1 y 15 → 3 consultas al optimizar | Correcto |

---

## Conclusión de la Parte 1

El hilo conductor es **dejar que la base de datos haga el trabajo, y hacerlo
de forma segura**: la transacción garantiza que una operación de tres pasos
se guarde completa o no se guarde, `F()` hace la resta en la base para no
perder descuentos simultáneos, `aggregate` y `annotate` arman el reporte sin
escribir SQL, el QuerySet propio escribe cada regla de negocio una sola vez,
y medir las consultas convierte el problema N+1 en números concretos: de 15
a 3 y de 6 a 1.
