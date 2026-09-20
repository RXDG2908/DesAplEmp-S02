# Tema 4 — Relaciones entre Models: 1:1, 1:N, N:M (Semana 4)

Este es el tema **más directamente conectado** con el Laboratorio 5: el
Django Admin de la Semana 5 no agrega relaciones nuevas, solo expone estas
tres que ya se implementaron aquí.

## Por qué relacionar entidades

Una app empresarial no trabaja con entidades aisladas: necesita conectar
datos de un mismo proceso de negocio (ejemplo del curso: Cliente, Pedido,
DetallePedido, Producto de una cafetería).

## La cardinalidad nace de las reglas del negocio

| Regla del negocio | Cardinalidad |
|---|---|
| Un cliente puede realizar varios pedidos | 1:N |
| Cada pedido pertenece a un solo cliente | N:1 |
| Un pedido puede contener varios productos | N:M |
| Cada perfil corresponde a un solo cliente | 1:1 |

## Django representa la cardinalidad con campos del Model

| Relación | Cardinalidad | Campo de Django |
|---|---|---|
| Uno a uno | 1:1 | `OneToOneField` |
| Uno a muchos | 1:N | `ForeignKey` |
| Muchos a muchos | N:M | `ManyToManyField` |

`Model → ORM → View → Template`: la relación se **define** en el Model, la
View la **consulta**, el Template la **presenta**.

## ForeignKey (1:N)

Se declara en el modelo que representa el lado "muchos".

```python
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="pedidos"
    )
```

Acceso en ambos sentidos gracias a `related_name`:

```python
pedido.cliente          # directo
cliente.pedidos.all()   # inverso
```

### on_delete — decisión de negocio, no solo técnica

| Opción | Comportamiento | Ejemplo de uso |
|---|---|---|
| `CASCADE` | Elimina también los objetos dependientes | Detalles de un pedido eliminado |
| `PROTECT` | Impide eliminar el objeto relacionado | Cliente con pedidos históricos |
| `SET_NULL` | Conserva el registro, borra la referencia (requiere `null=True`) | Relación opcional |

## OneToOneField (1:1)

```python
class PerfilCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, related_name="perfil"
    )
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
```

Acceso: `perfil.cliente` / `cliente.perfil`. Útil para separar información
complementaria (ficha, perfil) sin duplicar ni sobrecargar la entidad
principal — la entidad "solo existe si existe el registro principal, y como
máximo una por registro".

## ManyToManyField simple (N:M sin datos propios)

```python
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class Pedido(models.Model):
    productos = models.ManyToManyField(Producto)
```

Válido **solo** si la relación no necesita guardar información adicional
(cantidad, precio, fecha, estado...).

## ManyToManyField con modelo intermedio (`through`)

Cuando la relación sí necesita datos propios (que no pertenecen ni a una
entidad ni a la otra):

```python
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="detalles_pedido")
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
```

```python
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="pedidos")
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(
        Producto, through="DetallePedido", related_name="pedidos"
    )
```

`through` indica qué modelo administra la relación, en vez de depender de la
tabla automática que Django crearía por defecto.

## Migrar las relaciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Consultar relaciones desde la View

```python
def pedido_detalle(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects
            .select_related("cliente")
            .prefetch_related("detalles__producto"),
        id=pedido_id
    )
    return render(request, "pedidos/detalle.html", {"pedido": pedido})
```

- `select_related()` — para 1:1 y N:1 (hace un JOIN, una sola consulta).
- `prefetch_related()` — para colecciones / N:M (relación inversa o
  intermedia, consulta separada optimizada).

## Mostrar la relación en el Template

```django
<h2>Pedido de {{ pedido.cliente.nombre }}</h2>
{% for detalle in pedido.detalles.all %}
  <p>{{ detalle.producto.nombre }} — {{ detalle.cantidad }} unidad(es) — S/ {{ detalle.precio_unitario }}</p>
{% empty %}
  <p>El pedido todavía no tiene productos.</p>
{% endfor %}
```

## Tabla resumen (casos de repaso del PPT)

| Caso | Cardinalidad | Campo Django | Se declara en |
|---|---|---|---|
| Departamento–Empleado | 1:N | `ForeignKey` | Empleado (lado "muchos") |
| Estudiante–Curso | N:M | `ManyToManyField` | Cualquiera de los dos |
| Usuario–ConfiguracionCuenta | 1:1 | `OneToOneField` | ConfiguracionCuenta (la que extiende) |

`ManyToManyField` no lleva `on_delete`: Django administra automáticamente la
tabla intermedia (a diferencia de `ForeignKey`, ahí no hay una decisión de
negocio que tomar).

## Las tres relaciones ya implementadas en el proyecto real

**App `biblioteca`:**
- `CarnetSocio` **1:1** con `Socio` (`OneToOneField`, `CASCADE` — un carnet
  sin socio es un dato huérfano).
- `Categoria` → `Libro` **1:N** (`ForeignKey`, `PROTECT` — no se puede borrar
  una categoría con libros).
- `Socio` ←→ `Libro` **N:M** vía `Prestamo` (`through`, con `fecha_prestamo`,
  `fecha_devolucion_prevista`, `fecha_devolucion_real`, `estado`; ambas FK en
  `PROTECT` porque el historial de préstamos es contable).

**App `vet`:**
- `FichaClinica` **1:1** con `Cita` (`OneToOneField`, `CASCADE`).
- `Veterinario` → `Cita` **1:N** (`ForeignKey`, `SET_NULL` + `null=True` — si
  el veterinario se va, la cita queda "sin asignar" pero no se borra).
- `Cita` ←→ `Insumo` **N:M** vía `ConsumoInsumo` (`through`, con `cantidad` y
  `precio_unitario`; `CASCADE` en `cita`, `PROTECT` en `insumo`).

Estas son exactamente las entidades y relaciones que la **Semana 5** registra
en el Django Admin (Ejercicios 6 y 7 de la Parte 1: `StackedInline` para la
1:1, `TabularInline` para el modelo intermedio del N:M).
