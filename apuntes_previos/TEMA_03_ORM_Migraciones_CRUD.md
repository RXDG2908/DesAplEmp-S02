# Tema 3 — Persistencia, Models, Migraciones, ORM y CRUD (Semana 3)

## Memoria vs. persistencia

| Datos en memoria | Datos persistentes |
|---|---|
| Variable / lista Python | Django Model |
| Se pierden al reiniciar | Sobreviven al reiniciar |
| Sin estructura fija | Estructura definida por migraciones |
| Sin clave primaria | Clave primaria (`id`) automática |

El Laboratorio 3 convirtió la App de la Semana 2 (datos en lista, `forms.Form`)
en una App persistente: Model real + ORM + SQLite.

## Item.objects: el Manager

`objects` es el **Manager**: el punto de entrada habitual al ORM para
trabajar con los registros de un Model.

```
Item (Model) → objects (Manager) → all() / filter() / order_by()  → QuerySet
```

## QuerySets

```python
Item.objects.all()
Item.objects.filter(name__icontains='lap')
Item.objects.order_by('-created_at')
```

Las tres devuelven un **QuerySet**: una consulta sobre los registros. Django
construye la consulta y accede a la base solo cuando necesita los datos.

## Django ORM

Traduce operaciones Python (sobre instancias de un Model) en SQL, sin
escribir SQL directamente.

| Código Python | Equivale a |
|---|---|
| `Item.objects.all()` | `SELECT ...` |
| `Item.objects.create(...)` | `INSERT ...` |
| `item.save()` | `UPDATE ...` |
| `item.delete()` | `DELETE ...` |

## CRUD mediante Django ORM

| Operación | Django ORM | SQL conceptual |
|---|---|---|
| CREATE | `Item.objects.create(...)` | `INSERT` |
| READ | `Item.objects.all()/filter()/order_by()` | `SELECT` |
| UPDATE | `item.save()` | `UPDATE` |
| DELETE | `item.delete()` | `DELETE` |

```python
# UPDATE
item = Item.objects.get(id=1)
item.name = 'Laptop Gamer'
item.save()

# DELETE
item = Item.objects.get(id=1)
item.delete()
```

> Si DELETE se expone como vista web, debe dispararse con `POST`, nunca con
> `GET`.

## CRUD ≠ Migraciones

| CRUD — modifica **datos** | Migraciones — modifican **estructura** |
|---|---|
| `INSERT · SELECT · UPDATE · DELETE` | `CREATE TABLE · ALTER TABLE` |
| Crear/editar/eliminar un registro | Agregar un campo nuevo al Model |
| NO requiere migración | SÍ requiere `makemigrations` + `migrate` |

## makemigrations y migrate

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate core 0001
```

- `makemigrations` — detecta cambios en `models.py` y genera el archivo de
  migración (describe el cambio).
- `migrate` — aplica las migraciones pendientes sobre la base real.
- `showmigrations` — ver qué está aplicado (`[X]`) y qué pendiente (`[ ]`).
- `sqlmigrate` — ver el SQL exacto que generará una migración, sin aplicarlo.

Django registra el estado en la tabla interna `django_migrations`.

## SQLite

Base principal del curso: no requiere servidor, ni usuario/contraseña; el
archivo físico es `db.sqlite3` (no se sube al repo, está en `.gitignore`).

## Flujo completo — LISTAR (READ)

```
GET / → urls.py → item_list() → Item.objects.order_by()
    → QuerySet → Django ORM → SELECT → SQLite
    → Context → Template → Response
```

## Flujo completo — CREAR (CREATE) y Post/Redirect/Get

```
Formulario → POST /nuevo/ → item_create() → request.POST
    → Item.objects.create() → Django ORM → INSERT → SQLite
    → redirect() → GET / → lista actualizada
```

**Post/Redirect/Get:** tras un `POST` válido se redirige al listado (no se
renderiza directo). Evita que, al refrescar la página, el navegador reenvíe
el mismo `POST` y duplique el registro. No se usa JavaScript: la tabla se
actualiza porque Django redirige y vuelve a consultar la base.

## Adelanto: relaciones entre Models (se desarrolla en el Tema 4)

| Django | Relación |
|---|---|
| `ForeignKey` | 1 : N |
| `OneToOneField` | 1 : 1 |
| `ManyToManyField` | N : N |

## Ejemplo real — App `vet` (Laboratorio 3)

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

    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'
```

```python
def cita_list(request):
    citas = Cita.objects.order_by('fecha', 'hora')
    return render(request, 'vet/cita_list.html', {'citas': citas})

def cita_crear(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            Cita.objects.create(**form.cleaned_data)
            return redirect('vet:cita_list')
    else:
        form = CitaForm()
    return render(request, 'vet/cita_form.html', {'form': form})
```

`SERVICIOS`/`ESTADOS` van como `choices` en el propio campo (código) y no
como tabla aparte, porque son catálogos cerrados, no los administra el
usuario y no tienen datos propios — este mismo criterio se vuelve relevante
en la Semana 5 para decidir qué SÍ merece exponerse en el Django Admin.
