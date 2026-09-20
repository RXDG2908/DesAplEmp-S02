# Informe — Laboratorio 05: Administrador de Django (Django Admin)

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Lucas Inga - Renzo Leon

## PARTE 1 — Administrar en el Django Admin la aplicación de la Semana 4 (app `vet`)

### Ejercicio 1 — Recuperar la aplicación de la Semana 4

**App:** `vet` (reserva de citas de una veterinaria) — es la app guiada del
curso: nació sin base de datos en el Laboratorio 2, se persistió con Django
ORM/SQLite en el Laboratorio 3, y se amplió con las tres relaciones en el
Laboratorio 4.

**Entidad principal:** `Cita`, con los campos `mascota`, `dueno`, `servicio`,
`fecha`, `hora` y `estado`.

**Las tres relaciones implementadas en la Semana 4** (`vet/models.py`):

| Relación | Cardinalidad | Modelos | Campo Django | `on_delete` / `related_name` |
|---|---|---|---|---|
| Uno a uno | 1:1 | `Cita` ↔ `FichaClinica` | `OneToOneField` en `FichaClinica.cita` | `CASCADE`, `related_name='ficha'` |
| Uno a muchos | 1:N | `Veterinario` → `Cita` | `ForeignKey` en `Cita.veterinario` | `SET_NULL` + `null=True`, `related_name='citas'` |
| Muchos a muchos con modelo intermedio | N:M | `Cita` ↔ `Insumo` vía `ConsumoInsumo` | `ManyToManyField(..., through='ConsumoInsumo')` en `Cita.insumos` | `related_name='citas'`; FKs internas: `cita` (`CASCADE`), `insumo` (`PROTECT`) |

`ConsumoInsumo` guarda `cantidad` y `precio_unitario` — atributos que
pertenecen a la relación (cuánto insumo se usó y a qué precio en esa cita
concreta), no a `Cita` ni a `Insumo` por separado.

**Estado actual de las migraciones** (`python manage.py showmigrations vet`):

```
vet
 [X] 0001_initial
 [X] 0002_insumo_veterinario_fichaclinica_consumoinsumo_and_more
```

Ambas migraciones están **aplicadas**: `0001_initial` creó la tabla base
`vet_cita`; `0002_...` agregó `Insumo`, `Veterinario`, `FichaClinica`,
`ConsumoInsumo` y las columnas/FK de las tres relaciones. `db.sqlite3` ya
contiene esta estructura, no requiere una nueva migración para empezar el
Laboratorio 5 (el Django Admin no cambia el esquema, solo lo expone).

**Punto de partida en `admin.py`:** actualmente `vet/admin.py` no registra
ningún modelo (`# La App vet no usa el panel de administracion, no se
registra nada.`) — es el estado exacto que el Ejercicio 3 va a cambiar.

**Casos de prueba:**

| # | Caso | Resultado esperado | Resultado obtenido |
|---|------|--------------------|--------------------|
| 1 | `showmigrations vet` | `0001_initial` y `0002_...` aplicadas (`[X]`) | Correcto |
| 2 | Abrir `vet/admin.py` | Sin modelos registrados (Admin vacío para `vet`) | Correcto |
| 3 | Identificar la relación 1:1 | `FichaClinica.cita` (`OneToOneField`, `CASCADE`) | Correcto |
| 4 | Identificar la relación 1:N | `Cita.veterinario` (`ForeignKey`, `SET_NULL`) | Correcto |
| 5 | Identificar la relación N:M con `through` | `Cita.insumos` vía `ConsumoInsumo` | Correcto |

### Ejercicio 2 — Crear el superusuario

Se creó el superusuario `admin` con `python manage.py createsuperuser` (de
forma equivalente vía shell, usando `create_superuser` del modelo de
usuario — mismo resultado que el comando interactivo) y se inició sesión en
`/admin/`.

**Panel inicial del Django Admin**, ya con `vet` registrada junto a
`biblioteca`:

```
AUTENTICACIÓN Y AUTORIZACIÓN
  Grupos · Usuarios
BIBLIOTECA
  Bibliotecarios · Categorías · Editorials · Libros · Socios
CITAS VETERINARIA
  Citas · Insumos · Veterinarios
```

### Ejercicio 3 — Registrar los modelos en el Admin

En `vet/admin.py` se registraron los tres modelos principales con
`admin.site.register()`: `Cita`, `Veterinario`, `Insumo`. Los dos modelos de
la relación 1:1 y N:M (`FichaClinica`, `ConsumoInsumo`) **no se registran
aparte**: se exponen dentro de `Cita` mediante Inlines (Ejercicios 6 y 7),
que es la forma correcta de administrarlos porque no tiene sentido un listado
independiente de fichas clínicas sueltas o de consumos sueltos — siempre
pertenecen a una Cita concreta.

```python
# vet/admin.py
from django.contrib import admin
from .models import Cita, ConsumoInsumo, FichaClinica, Insumo, Veterinario

admin.site.register(Cita, CitaAdmin)
admin.site.register(Veterinario, VeterinarioAdmin)
admin.site.register(Insumo)
```

### Ejercicio 4 — Personalizar con `ModelAdmin`

Dos modelos reemplazaron el registro simple por una clase `ModelAdmin`:

```python
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'dueno', 'servicio', 'fecha', 'hora', 'estado', 'veterinario')
    search_fields = ('mascota', 'dueno')
    list_filter = ('estado', 'servicio', 'fecha')
    inlines = [FichaClinicaInline, ConsumoInsumoInline]

class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'colegiatura', 'especialidad')
    search_fields = ('nombre', 'colegiatura')
```

Verificado en el navegador: el listado de `Citas` muestra las columnas de
`list_display` (mascota, dueño, servicio, fecha, hora, estado, veterinario) y
la caja de búsqueda funciona sobre `mascota`/`dueno`.

### Ejercicio 5 — Agregar `list_filter`

`list_filter = ('estado', 'servicio', 'fecha')` en `CitaAdmin`. Verificado:
el panel lateral del Admin muestra los filtros **Por estado** (Pendiente /
Confirmada / Atendida), **Por servicio** (Consulta / Vacunación / Cirugía /
Baño) y **Por fecha** (Hoy / Últimos 7 días / Este mes / Este año),
funcionando sobre datos reales cargados en `db.sqlite3`.

### Ejercicio 6 — Exponer la relación 1:1 con `StackedInline`

```python
class FichaClinicaInline(admin.StackedInline):
    model = FichaClinica
    extra = 0
```

Verificado: al abrir una `Cita` desde el Admin aparece la sección "Ficha
clínica" con los campos `peso_kg`, `diagnostico`, `tratamiento`,
`proximo_control` editables en la misma pantalla, sin necesidad de una View
propia.

### Ejercicio 7 — Exponer la relación N:M con `TabularInline`

```python
class ConsumoInsumoInline(admin.TabularInline):
    model = ConsumoInsumo
    extra = 1
```

Verificado: dentro de la pantalla de `Cita` aparece la tabla "Consumos de
insumos" con columnas `Insumo`, `Cantidad`, `Precio unitario` — los
atributos propios del modelo intermedio `ConsumoInsumo` — editables fila por
fila, más un botón para agregar filas adicionales.

### Ejercicio 8 — Verificar el flujo completo en el Admin

Se realizó una operación real de creación/edición desde el panel: sobre la
cita "Michi" (Ana Torres, Vacunación) se completó por primera vez su
**Ficha Clínica** (peso `4.2`, diagnóstico "Sano, aplicada vacuna
antirrábica") usando el `StackedInline`, y se confirmó que el consumo de
insumo ya cargado (`Jeringa 5ml`, cantidad 1, S/ 1.50) mediante el
`TabularInline` se conservó al guardar. El Admin devolvió el mensaje "El
cita 'Michi - Vacunación (...)' se cambió correctamente" y el listado
reflejó el cambio de inmediato — la misma lógica de Post/Redirect/Get vista
en la Semana 3, pero generada automáticamente por Django, sin escribir
`views.py` ni `urls.py` para esta pantalla.

**Qué resuelve el Django Admin vs. qué seguiría necesitando una View y un
Template propios:**

El Admin resuelve, sin escribir código de presentación, el CRUD completo de
`Cita` y de sus relaciones (StackedInline para la 1:1, TabularInline para el
N:M con `through`), reutilizando exactamente el mismo Model y el mismo ORM
que ya existían desde la Semana 3-4 — no crea una tabla nueva, no cambia
`models.py`. Sin embargo, el Admin está pensado para el **staff** (usuarios
con permisos de administración), no para el cliente final: no permite, por
ejemplo, que un dueño de mascota reserve su propia cita desde una pantalla
pública, no controla el diseño visual que vería ese usuario, ni aplica
reglas de negocio específicas del flujo público (como el `clean()` que
evitaba citas duplicadas en el mismo horario, visto en semanas previas). Para
eso seguiría siendo necesaria una View y un Template propios, tal como los
que ya existen en `vet/views.py` para el listado y la creación de citas
desde el sitio público.

**Casos de prueba (Ejercicios 2-8):**

| # | Caso | Resultado esperado | Resultado obtenido |
|---|------|--------------------|--------------------|
| 1 | Login en `/admin/` con el superusuario creado | Redirige al panel del Admin | Correcto |
| 2 | Panel inicial del Admin | Aparecen `Citas`, `Insumos`, `Veterinarios` bajo "Citas veterinaria" | Correcto |
| 3 | Buscar una cita por nombre de mascota/dueño | El listado filtra por `search_fields` | Correcto |
| 4 | Filtrar por estado/servicio/fecha en el panel lateral | El listado se reduce según `list_filter` | Correcto |
| 5 | Abrir una `Cita` existente | Aparece el Inline "Ficha clínica" (vacío si no se ha atendido) | Correcto |
| 6 | Abrir una `Cita` con consumos ya cargados | Aparece el Inline "Consumos de insumos" con filas editables | Correcto |
| 7 | Completar la Ficha Clínica de una cita y guardar | El Admin confirma el cambio y conserva el/los consumo(s) ya cargados | Correcto |

---

## PARTE 2 — Administrar la investigación propia (app `biblioteca`)

Pendiente de desarrollar en los siguientes ejercicios. Punto de partida
verificado:

- `biblioteca/admin.py` ya registra `Bibliotecario`, `Editorial`, `Socio`,
  `Categoria` y `Libro` con `admin.site.register()` simple (sin
  personalizar).
- **Faltan por registrar** las dos entidades agregadas en la Semana 4:
  `CarnetSocio` (1:1 con `Socio`) y `Prestamo` (modelo intermedio N:M de
  `Socio` ↔ `Libro`) — con eso se completan las 7 entidades que pide el
  checklist de la Parte 2.
- Migraciones (`showmigrations biblioteca`): `0001_initial` y
  `0002_carnetsocio_prestamo_socio_libros`, ambas `[X]` aplicadas.

Ejercicios 9-14 de la Parte 2: **pendientes** — ver
[LUCAS_TODO_Lab05.md](LUCAS_TODO_Lab05.md) para el detalle de lo que falta
completar sobre `biblioteca`.

## Conclusiones (Parte 1 — Ejercicios 1 a 8, app `vet`)

- Django Admin no requiere migraciones nuevas: se apoya en la estructura que
  ya existe desde la Semana 4.
- Las tres relaciones (1:1, 1:N, N:M con `through`) ya implementadas en
  `vet/models.py` se registraron y personalizaron sin tocar `models.py`: el
  trabajo de este laboratorio es de **registro y personalización**
  (`ModelAdmin`, `list_display`, `search_fields`, `list_filter`,
  `StackedInline`, `TabularInline`), no de modelado de datos.
- `FichaClinica` y `ConsumoInsumo` no se registran como entradas propias del
  Admin: se exponen únicamente como Inlines dentro de `Cita`, porque no
  tienen sentido fuera de la Cita a la que pertenecen.
- El flujo completo (login → listado con filtros/búsqueda → edición con
  Inlines → guardar) se verificó en el navegador contra datos reales del
  proyecto, no solo leyendo el código.
- Nota aparte (no forma parte del alcance de este laboratorio): al editar la
  cita "Michi" el campo `Servicio` llegó vacío en el formulario porque el
  valor guardado en `db.sqlite3` tiene un problema de codificación
  (`VacunaciÃ³n` en vez de `Vacunación`), heredado del script de carga de
  datos de semanas anteriores. Se corrigió manualmente para esa fila al
  guardar; si aparece en más registros, es un tema de datos de prueba, no
  del Django Admin.
