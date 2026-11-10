# Exposición — Laboratorio 07, Parte 1: ORM avanzado sobre la app `vet`

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** usar el ORM de Django más allá del CRUD: registrar una operación
segura con transacciones, calcular reportes, encapsular reglas del negocio en
un QuerySet propio y reducir el número de consultas a la base de datos.

> Este documento explica, en el orden en que se hicieron, todos los pasos de
> la Parte 1 del Laboratorio 7. La idea es poder exponérselo al profesor
> contando la historia completa: de dónde veníamos, qué se hizo en cada paso
> y por qué, sin necesitar leer el código en paralelo.

---

## De dónde partimos

Antes de este laboratorio la app `vet` ya tenía: un Model `Cita` guardado en
SQLite (Laboratorio 3), sus tres relaciones (Laboratorio 4) —la ficha clínica
**uno a uno**, el veterinario **uno a muchos** y los insumos **muchos a
muchos** a través del modelo intermedio `ConsumoInsumo`—, el registro en el
Django Admin (Laboratorio 5) y los Templates con herencia de `base.html`
(Laboratorio 6).

Hasta aquí el ORM se había usado para lo básico: crear, listar, ver el
detalle y recorrer relaciones. En este laboratorio **no se creó ninguna
entidad nueva**: se aprovecharon las que ya existían para cuatro cosas que
pide cualquier aplicación empresarial real:

1. Registrar una operación que toca **varios modelos a la vez** sin dejar
   datos a medias.
2. Sacar **totales y conteos** sin escribir SQL.
3. Guardar las **reglas del negocio** en un solo lugar.
4. Que las pantallas no hagan **una consulta por cada fila**.

El recorrido de una petición queda así:

```
Cliente (navegador) → URL (ej. /reporte/) → vet/urls.py → View
→ CitaQuerySet (Manager personalizado) → Django ORM (aggregate / annotate)
→ SQLite → Template que hereda de base.html → Response
```

---

## Paso 1 — Ubicar los campos clave (Ejercicio 1)

La guía pide identificar la entidad principal, sus tres relaciones y tres
campos. Con la tabla de equivalencias (en clase el ejemplo era una tienda con
productos y pedidos):

| Concepto de la clase | En la app `vet` |
|---|---|
| Campo entero que se descuenta (stock del producto) | `Insumo.stock` |
| Campo de estado (estado del pedido) | `Cita.estado`: Pendiente, Confirmada, Atendida |
| Atributos del modelo intermedio (cantidad, precio) | `ConsumoInsumo.cantidad` y `ConsumoInsumo.precio_unitario` |
| Operación que modifica varios modelos | Registrar un consumo de insumo en una cita |

Los tres campos **ya existían** desde la Semana 4, así que no hizo falta
tocar `models.py`. Se comprobó con:

```powershell
python manage.py makemigrations --check --dry-run   # No changes detected
python manage.py showmigrations vet                 # 0001 y 0002 aplicadas
```

---

## Paso 2 — Datos de prueba (Ejercicio 2)

Para que los reportes muestren algo, la guía pide al menos 5 citas, 3
veterinarios y 8 registros del modelo intermedio. Se escribió el script
`cargar_lab07.py` (en `src`), que usa `get_or_create()` para que se pueda
ejecutar varias veces **sin duplicar** nada:

```powershell
python manage.py shell -c "exec(open('cargar_lab07.py', encoding='utf-8').read())"
# Citas: 5 | Veterinarios: 3 | Insumos: 4 | Consumos: 8
```

Quedaron citas con los tres estados (Rocky y Nala Atendidas, Michi y Toby
Confirmadas, Luna Pendiente). Las de Luna y Toby tienen fecha de fines de
octubre para que haya citas "próximas". Todo se revisó en el Admin: el
listado de citas, el de veterinarios y los consumos dentro de cada cita.

---

## Paso 3 — Una operación segura con `transaction.atomic()` y `F()` (Ejercicio 3)

Se creó la pantalla **Registrar consumo** (`/consumo/nuevo/`), con su ruta en
`vet/urls.py`, la vista `consumo_registrar` en `vet/views.py`, el formulario
`ConsumoForm` en `vet/forms.py` y el Template `consumo_form.html`, que hereda
de `base.html`.

Registrar un consumo toca **tres modelos**: se crea el `ConsumoInsumo`, la
`Cita` pasa a Atendida y al `Insumo` se le descuenta el stock. El riesgo es
que algo falle a la mitad y quede, por ejemplo, el consumo creado pero el
stock sin descontar. Por eso las tres operaciones van juntas:

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

- **`transaction.atomic()`**: o se guarda todo o no se guarda nada. Si
  dentro del bloque se lanza un error, Django deshace también lo que ya se
  había hecho antes (el consumo creado y el cambio de estado).
- **`F('stock') - cantidad`**: la resta la hace la **base de datos**, no
  Python. Si se leyera el stock, se restara en Python y se guardara, dos
  registros al mismo tiempo podrían pisarse y perder un descuento.
- **`stock__gte=cantidad`**: el descuento solo se aplica si alcanza. Si no
  alcanza, `update()` devuelve 0 filas y se lanza el error.
- Si sale bien, se aplica **Post/Redirect/Get**: se redirige al detalle de
  la cita, así recargar la página no vuelve a registrar el consumo.

Se probaron los dos casos con la jeringa de 5 ml (stock inicial 100):

| Caso | Resultado | Citas | Consumos | Stock |
|---|---|---|---|---|
| Antes | — | 5 | 8 | 100 |
| Toby, 2 jeringas | Redirige al detalle; Toby queda Atendida | 5 | 9 | 98 |
| Luna, 9999 jeringas | Mensaje "Stock insuficiente de Jeringa 5ml" | 5 | 9 | 98 |

En el caso que falla **nada cambió**: ni se creó el consumo ni Luna pasó a
Atendida. Eso demuestra que el rollback funcionó.

---

## Paso 4 — Un total con `aggregate()` (Ejercicio 4)

En el shell se calculó cuánto se consumió en total, multiplicando cantidad
por precio en cada fila del modelo intermedio y sumando:

```python
>>> ConsumoInsumo.objects.aggregate(
...     total=Sum(F('cantidad') * F('precio_unitario'), output_field=DecimalField()))
{'total': Decimal('110.5')}
```

**¿Por qué `aggregate()` no devuelve un QuerySet?** Porque resume **toda la
tabla en un solo valor**. Un QuerySet es una colección de objetos del Model;
un total no es un objeto, así que Django devuelve un diccionario simple. Por
eso es una consulta final: después ya no se puede seguir filtrando ni
ordenando.

---

## Paso 5 — Valores por objeto con `annotate()` (Ejercicio 5)

`annotate()` calcula un valor **por cada objeto** y el resultado sigue
siendo un QuerySet:

```python
>>> for c in Cita.objects.annotate(n=Count('consumos')).order_by('-n'):
...     print(c.mascota, c.n)
Rocky 3 · Luna 2 · Toby 2 · Michi 1 · Nala 1
```

Y combinado con `values()` agrupa, como un `GROUP BY`:

```python
>>> Cita.objects.values('estado').annotate(total=Count('id')).order_by('-total')
Atendida 3 · Pendiente 1 · Confirmada 1
```

| | `aggregate()` | `annotate()` |
|---|---|---|
| Qué calcula | Un valor para toda la tabla | Un valor por cada objeto o grupo |
| Qué devuelve | Un diccionario | Un QuerySet (se puede seguir encadenando) |
| Ejemplo | Total consumido: 110.50 | Consumos por cita, citas por estado |

---

## Paso 6 — La página de reporte (Ejercicio 6)

Se creó la ruta `/reporte/`, la vista `reporte` y el Template `reporte.html`,
que hereda de `base.html`. La vista junta los cálculos de los pasos 4 y 5 y
los manda al Template:

- total global consumido → **S/ 110,50**
- consumos por cita y citas por estado (dos tablas)
- citas próximas pendientes → **1** (la de Luna)

En el Template se usa el filtro `{{ total|floatformat:2 }}`, para que el
total siempre salga con dos decimales, como un precio. Además se agregaron
en el menú de `base.html` los enlaces **Registrar consumo** y **Reporte**.

---

## Paso 7 — Un QuerySet personalizado (Ejercicio 7)

Filtros como "citas con tal estado" o "citas de hoy en adelante" se repetían
en varias vistas. Se movieron a `vet/models.py` como métodos de un QuerySet
propio:

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

Con `as_manager()` estos métodos quedan disponibles en `Cita.objects` y se
pueden **encadenar**, igual que `filter()`. Se usan en dos vistas:

- `cita_list`: si llega `?estado=Pendiente` en la URL, aplica
  `citas.con_estado(estado)`.
- `reporte`: `Cita.objects.proximas().con_estado('Pendiente').count()`.

La ventaja es que la regla del negocio vive en **un solo lugar**: si mañana
"próximas" significa "de esta semana", se cambia una línea y todas las
vistas se actualizan. Se verificó que el listado, el filtro por estado y el
detalle siguen funcionando, es decir, el CRUD de la Semana 3 no se rompió.

---

## Paso 8 — El problema N+1 (Ejercicio 8)

Cuando una pantalla muestra datos de una relación, Django por defecto hace
**una consulta para la lista y otra más por cada fila** para traer el dato
relacionado. Con muchas filas, eso se vuelve lento. Se midió con el script
`medir_n1.py` (en `src`), que usa `reset_queries()` y
`len(connection.queries)` con `DEBUG=True`:

```powershell
python manage.py shell -c "exec(open('medir_n1.py', encoding='utf-8').read())"
```

| Pantalla | Sin optimizar | Optimizada |
|---|---|---|
| Citas con su veterinario | 6 consultas (1 + 5 citas) | **1** con `select_related` |
| Citas con sus consumos e insumos | 15 consultas (1 + 5 + 9) | **3** con `prefetch_related` |

**¿Cuándo usar cada uno?**

- **`select_related()`** → relaciones **de a uno** (ForeignKey y
  OneToOne). Hace un JOIN y trae todo en una sola consulta. En la app: el
  veterinario y la ficha de cada cita, en `cita_list`.
- **`prefetch_related()`** → relaciones **de a muchos** (ManyToMany y el
  lado inverso de una ForeignKey). Hace una consulta por relación y une los
  resultados en Python, porque un JOIN repetiría las filas. En la app: los
  consumos y sus insumos, en `cita_detalle`.

---

## Cómo se verificó cada paso (resumen de pruebas)

| Ejercicio | Cómo se verificó | Resultado |
|---|---|---|
| 1 | `makemigrations --check` y `showmigrations` | Sin cambios pendientes |
| 2 | Script de carga + Admin | 5 citas, 3 veterinarios, 8 consumos |
| 3 | Formulario en el navegador + conteos en el shell | Éxito 8→9 y 100→98; falla sin cambios |
| 4 | Shell | `{'total': Decimal('110.5')}` |
| 5 | Shell | Rocky 3 … Nala 1; Atendida 3, Pendiente 1, Confirmada 1 |
| 6 | `/reporte/` en el navegador | S/ 110,50 y 1 cita próxima pendiente |
| 7 | `/?estado=Pendiente`, `/?estado=Atendida`, detalle | Filtra bien; CRUD intacto |
| 8 | `medir_n1.py` | 6 → 1 y 15 → 3 consultas |

---

## Archivos que se tocaron

| Archivo | Qué tiene del Lab 7 |
|---|---|
| `vet/models.py` | `CitaQuerySet` con `con_estado()` y `proximas()`, asignado con `as_manager()` |
| `vet/views.py` | `consumo_registrar` (transacción y `F()`), `reporte` (aggregate y annotate), `cita_list` usa `con_estado()` |
| `vet/forms.py` | `ConsumoForm` |
| `vet/urls.py` | rutas `consumo/nuevo/` y `reporte/` |
| `templates/vet/consumo_form.html` | formulario que muestra el error de stock |
| `templates/vet/reporte.html` | reporte con `floatformat:2` |
| `templates/base.html` | enlaces del menú y pie "Laboratorio 07" |
| `cargar_lab07.py`, `medir_n1.py` | carga de datos y medición de consultas |

---

## Conclusión de la Parte 1

- Una operación que toca varios modelos va dentro de `transaction.atomic()`:
  si el stock no alcanza, no se guarda nada.
- `F()` hace la resta dentro de la base de datos y evita perder descuentos
  cuando dos registros ocurren a la vez.
- `aggregate()` resume la tabla en un valor y `annotate()` calcula un valor
  por objeto o grupo; con ambos se armó el reporte sin escribir SQL.
- Un QuerySet personalizado concentra las reglas del negocio y permite
  encadenarlas.
- Medir las consultas deja ver el N+1 con números: de 15 se bajó a 3 y de 6
  a 1.
- Todo esto se reutiliza en el Laboratorio 8: la API de citas filtra con
  `con_estado()`, su acción `proximas` llama a `proximas()` y su
  `get_queryset()` usa `select_related` y `prefetch_related`.
