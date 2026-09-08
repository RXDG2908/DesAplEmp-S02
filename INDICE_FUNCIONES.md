# Índice de funciones y sondeo del código — Proyecto `django_project`

Curso **Desarrollo de Aplicaciones Empresariales** (4 - C24 - Sección CD).
Este documento recorre **cada archivo, clase y función** del proyecto y lo nombra
con el vocabulario visto en el material del curso: **Project / App**, patrón
**MVT** (Model–View–Template), ciclo **Request → Response**, **URLs y Views**,
**Models y ORM**, **migraciones**, **Templates y Context** ([CLAUDE.md](CLAUDE.md),
Sesión 02) y el **flujo CRUD completo** `Request → URL → View → Model →
Manager/QuerySet → Django ORM → SQLite → Template → Response`
([GLAB-S03.md](GLAB-S03.md)).

Solo se usan conceptos presentes en `CLAUDE.md`, `GLAB-S02.md`, `GLAB-S03.md`,
`README.md`, `INFORME_Lab02.md` e `INFORME_Lab03.md`.

---

## 1. Mapa del proyecto

```
django_project/src/
├── config/       → EL PROJECT (configuración, sin lógica de negocio)
├── vet/          → APP 1  · Reserva de citas de veterinaria   (Lab 02 → Lab 03 Parte 1)
├── biblioteca/   → APP 2  · Catálogo de biblioteca comunitaria (Lab 03 Parte 2)
└── templates/    → Templates (la "T" de MVT), compartidos por las dos Apps
```

| Concepto del material | Dónde está en el código |
|---|---|
| Project (contenedor de configuración) | `config/` |
| App (módulo funcional reutilizable) | `vet/`, `biblioteca/` |
| Model (datos) | `vet/models.py`, `biblioteca/models.py` |
| View (procesamiento del request) | `vet/views.py`, `biblioteca/views.py` |
| Template (presentación / HTML) | `templates/` |
| URLs (enrutamiento, "director de tráfico") | `config/urls.py`, `vet/urls.py`, `biblioteca/urls.py` |
| ORM (objetos Python ↔ SQL) | `Cita.objects…`, `Libro.objects…`, Class-Based Views |
| Migraciones (estructura de la BD) | `vet/migrations/`, `biblioteca/migrations/` |

---

## 2. `config/` — el Project

| Archivo | Elemento | Rol (según el material) |
|---|---|---|
| [config/settings.py](django_project/src/config/settings.py) | `INSTALLED_APPS` | Registra las Apps propias: `'vet'`, `'biblioteca'`. |
| | `DATABASES` (`ENGINE: sqlite3`) | Motor de persistencia de la Semana 3. |
| | `ROOT_URLCONF = 'config.urls'` | Punto de entrada del enrutamiento. |
| | `TEMPLATES` | Dónde busca Django los Templates. |
| [config/urls.py](django_project/src/config/urls.py) | `urlpatterns` | Enrutado raíz del Project. |

`urlpatterns` de `config/urls.py`:

| Patrón | Destino | Explicación |
|---|---|---|
| `admin/` | `admin.site.urls` | Django Admin. |
| `''` | `include('vet.urls')` | La raíz `/` la maneja la App `vet`. |
| `biblioteca/` | `include('biblioteca.urls')` | Todo lo que empieza con `/biblioteca/` lo maneja la App `biblioteca`. |

`include(...)` = delegar el enrutado a la tabla de rutas **propia de cada App**
(URLs y Views, `CLAUDE.md` §5–6).

---

## 3. App `vet` — Reserva de citas

Entidad principal: **`Cita`**. En la Semana 2 los datos vivían en una lista en
memoria; en la Semana 3 se convirtió en un **Django Model** persistido en SQLite
(`INFORME_Lab03.md`, Ej. 1–5).

### 3.1 `vet/models.py` — la "M" de MVT

| Elemento | Ubicación | Descripción |
|---|---|---|
| `class Cita(models.Model)` | [vet/models.py:11](django_project/src/vet/models.py:11) | Se mapea a la tabla `vet_cita`. Django agrega solo el campo `id` como clave primaria. |
| `Cita.SERVICIOS` | [vet/models.py:28](django_project/src/vet/models.py:28) | Catálogo cerrado (Consulta / Vacunación / Cirugía / Baño) usado como `choices`, **no** como tabla (justificación del profesor, `INFORME_Lab03.md` Ej. 2). |
| `Cita.ESTADOS` | [vet/models.py:34](django_project/src/vet/models.py:34) | Catálogo cerrado (Pendiente / Confirmada / Atendida). |
| Campos `mascota, dueno, servicio, fecha, hora, estado` | [vet/models.py:41](django_project/src/vet/models.py:41) | Cada atributo `models.*` = una columna. `estado` tiene `default='Pendiente'`. |
| `def __str__(self)` | [vet/models.py:52](django_project/src/vet/models.py:52) | Cómo se "ve" una Cita en el shell y en el admin. |

Tipos: `CharField`, `DateField`, `TimeField` (`CLAUDE.md` §7).

### 3.2 `vet/forms.py` — captura de datos del Request

| Elemento | Ubicación | Descripción |
|---|---|---|
| `class CitaForm(forms.Form)` | [vet/forms.py:13](django_project/src/vet/forms.py:13) | Hereda de `forms.Form` (no `ModelForm`), tal como indica el material de la semana. Define **qué** datos pide y **cómo** se validan. |
| Campos `mascota, dueno, servicio, fecha, hora` | [vet/forms.py:24](django_project/src/vet/forms.py:24) | `servicio` toma sus opciones de `Cita.SERVICIOS` (una sola fuente de verdad). `fecha`/`hora` usan `widget` con `type=date`/`type=time`. |
| `def clean(self)` | [vet/forms.py:43](django_project/src/vet/forms.py:43) | Validación entre varios campos: consulta la tabla con `Cita.objects.filter(fecha=…, hora=…)` (ORM) y evita dos citas en el mismo horario. |

### 3.3 `vet/views.py` — la "V" de MVT (procesamiento, similar a un Controller)

| Función | Ubicación | Operación | Flujo (según `GLAB-S03.md` Ej. 6) |
|---|---|---|---|
| `cita_list(request)` | [vet/views.py:12](django_project/src/vet/views.py:12) | **READ** | `GET /` → `Cita.objects.order_by('fecha','hora')` → QuerySet → ORM → `SELECT` → SQLite → Context `{'citas': citas}` → `cita_list.html` → Response. |
| `cita_crear(request)` | [vet/views.py:22](django_project/src/vet/views.py:22) | **CREATE** | `GET /nueva/` muestra `CitaForm()` vacío. `POST` válido → `Cita.objects.create(...)` → ORM → `INSERT` → SQLite → `redirect('vet:cita_list')` (**Post/Redirect/Get**). |

### 3.4 `vet/urls.py` — la tabla de rutas de la App

| Elemento | Ubicación | Descripción |
|---|---|---|
| `app_name = 'vet'` | [vet/urls.py:11](django_project/src/vet/urls.py:11) | Namespace: permite `vet:cita_list` en Templates y `redirect()`. |
| `path('', views.cita_list, name='cita_list')` | [vet/urls.py:20](django_project/src/vet/urls.py:20) | Raíz de la App → listado. |
| `path('nueva/', views.cita_crear, name='cita_crear')` | [vet/urls.py:21](django_project/src/vet/urls.py:21) | Formulario de registro. |

### 3.5 Otros archivos de la App `vet`

| Archivo | Elemento | Descripción |
|---|---|---|
| [vet/apps.py:8](django_project/src/vet/apps.py:8) | `class VetConfig(AppConfig)` | Configuración de la App. `name = 'vet'`, `verbose_name = 'Citas veterinaria'`, `default_auto_field = BigAutoField` (el `id` que Django agrega solo). |
| [vet/admin.py](django_project/src/vet/admin.py) | — | Sin modelos registrados (la App `vet` no usa el panel de administración). |
| [vet/migrations/0001_initial.py](django_project/src/vet/migrations/0001_initial.py) | `CreateModel(name='Cita')` | Migración que crea la tabla `vet_cita` (`makemigrations` → `migrate`, `INFORME_Lab03.md` Ej. 3). |

---

## 4. App `biblioteca` — Catálogo de la biblioteca comunitaria

Cinco entidades (`GLAB-S03.md` Ej. 9): **tres independientes**
(Bibliotecario, Editorial, Socio) y **dos relacionadas por `ForeignKey`**
(Categoria 1 ──< Libro N). CRUD completo con **Class-Based Views** genéricas de
Django, todo mediante ORM y SQLite.

### 4.1 `biblioteca/models.py` — los cinco Models

| Model | Ubicación | Tipo | Campos | Relación |
|---|---|---|---|---|
| `Bibliotecario` | [biblioteca/models.py:17](django_project/src/biblioteca/models.py:17) | Independiente | `nombre`, `dni` (único), `turno` (`choices` `TURNOS`) | — |
| `Editorial` | [biblioteca/models.py:32](django_project/src/biblioteca/models.py:32) | Independiente | `nombre`, `pais` | — |
| `Socio` | [biblioteca/models.py:41](django_project/src/biblioteca/models.py:41) | Independiente | `nombre`, `dni` (único), `telefono` (`blank=True`) | — |
| `Categoria` | [biblioteca/models.py:51](django_project/src/biblioteca/models.py:51) | Lado **"1"** | `nombre` (único), `descripcion` (`blank=True`); `Meta.verbose_name_plural` | Una Categoria tiene muchos Libros |
| `Libro` | [biblioteca/models.py:63](django_project/src/biblioteca/models.py:63) | Lado **"N"** | `titulo`, `autor`, `isbn` (único), `anio_publicacion` (`PositiveIntegerField`), `categoria` (`ForeignKey`) | `ForeignKey(Categoria, on_delete=PROTECT, related_name='libros')` |

Cada Model define su `__str__`. `on_delete=PROTECT` = no se puede borrar una
Categoria mientras tenga Libros (requisito funcional 11, `INFORME_Lab03.md` Ej. 8).
`related_name='libros'` permite `categoria.libros.all()` (Ej. 9).

### 4.2 `biblioteca/views.py` — 20 Views (5 entidades × 4 operaciones CRUD)

Todas son **Class-Based Views** genéricas: `ListView` (READ / `SELECT`),
`CreateView` (CREATE / `INSERT`), `UpdateView` (UPDATE / `UPDATE`),
`DeleteView` (DELETE / `DELETE`, con confirmación por `POST`).

| Entidad | ListView | CreateView | UpdateView | DeleteView |
|---|---|---|---|---|
| Bibliotecario | `BibliotecarioListView` [:15](django_project/src/biblioteca/views.py:15) | `BibliotecarioCreateView` [:21](django_project/src/biblioteca/views.py:21) | `BibliotecarioUpdateView` [:29](django_project/src/biblioteca/views.py:29) | `BibliotecarioDeleteView` [:37](django_project/src/biblioteca/views.py:37) |
| Editorial | `EditorialListView` [:46](django_project/src/biblioteca/views.py:46) | `EditorialCreateView` [:52](django_project/src/biblioteca/views.py:52) | `EditorialUpdateView` [:60](django_project/src/biblioteca/views.py:60) | `EditorialDeleteView` [:68](django_project/src/biblioteca/views.py:68) |
| Socio | `SocioListView` [:77](django_project/src/biblioteca/views.py:77) | `SocioCreateView` [:83](django_project/src/biblioteca/views.py:83) | `SocioUpdateView` [:91](django_project/src/biblioteca/views.py:91) | `SocioDeleteView` [:99](django_project/src/biblioteca/views.py:99) |
| Categoria | `CategoriaListView` [:108](django_project/src/biblioteca/views.py:108) | `CategoriaCreateView` [:114](django_project/src/biblioteca/views.py:114) | `CategoriaUpdateView` [:122](django_project/src/biblioteca/views.py:122) | `CategoriaDeleteView` [:130](django_project/src/biblioteca/views.py:130) |
| Libro | `LibroListView` [:139](django_project/src/biblioteca/views.py:139) | `LibroCreateView` [:146](django_project/src/biblioteca/views.py:146) | `LibroUpdateView` [:154](django_project/src/biblioteca/views.py:154) | `LibroDeleteView` [:162](django_project/src/biblioteca/views.py:162) |

`LibroListView` usa `Libro.objects.select_related('categoria').order_by('titulo')`:
un QuerySet que trae cada Libro **con su Categoria** (la relación ForeignKey) y
ordenado por título (`Model.objects.order_by(...)`, `GLAB-S03.md` Ej. 15).

### 4.3 `biblioteca/urls.py` — 20 rutas

`app_name = 'biblioteca'`. Por cada entidad, cuatro `path()`:

| Ruta | Nombre | View | Operación |
|---|---|---|---|
| `<entidad>/` | `<entidad>_list` | `…ListView` | READ |
| `<entidad>/nuevo/` | `<entidad>_crear` | `…CreateView` | CREATE |
| `<entidad>/<int:pk>/editar/` | `<entidad>_editar` | `…UpdateView` | UPDATE |
| `<entidad>/<int:pk>/eliminar/` | `<entidad>_eliminar` | `…DeleteView` | DELETE |

Definidas en [biblioteca/urls.py:7](django_project/src/biblioteca/urls.py:7)
(bibliotecarios), `:13` (editoriales), `:18` (socios), `:23` (categorias),
`:28` (libros). El `<int:pk>` es el parámetro que la URL le pasa a la View para
saber **qué registro** editar o eliminar.

### 4.4 Otros archivos de la App `biblioteca`

| Archivo | Elemento | Descripción |
|---|---|---|
| [biblioteca/admin.py](django_project/src/biblioteca/admin.py) | `admin.site.register(...)` ×5 | Registra los cinco Models en el Django Admin. |
| [biblioteca/apps.py:4](django_project/src/biblioteca/apps.py:4) | `class BibliotecaConfig(AppConfig)` | `name = 'biblioteca'`. |
| [biblioteca/migrations/0001_initial.py](django_project/src/biblioteca/migrations/0001_initial.py) | `CreateModel` ×5 | Crea `biblioteca_bibliotecario`, `_categoria`, `_editorial`, `_socio`, `_libro`. El `Libro` incluye la `ForeignKey` a `biblioteca.categoria` con `on_delete=PROTECT`. |

---

## 5. `templates/` — la "T" de MVT

| Template | Usado por | Context que recibe |
|---|---|---|
| [base.html](django_project/src/templates/base.html) | Todos (herencia con `{% extends %}`) | — |
| [vet/cita_list.html](django_project/src/templates/vet/cita_list.html) | `cita_list` | `{'citas': QuerySet}` → `{% for cita in citas %}` |
| [vet/cita_form.html](django_project/src/templates/vet/cita_form.html) | `cita_crear` | `{'form': CitaForm}` |
| `biblioteca/<entidad>_list.html` ×5 | `…ListView` | `{'objetos': QuerySet}` (`context_object_name = 'objetos'`) |
| [biblioteca/generic_form.html](django_project/src/templates/biblioteca/generic_form.html) | `…CreateView` / `…UpdateView` | `form` + `titulo` (`extra_context`) |
| [biblioteca/generic_confirm_delete.html](django_project/src/templates/biblioteca/generic_confirm_delete.html) | `…DeleteView` | `object` — pantalla de **confirmación** antes del `POST` |

**Context** = el diccionario que la View envía al Template; cada clave queda
disponible como variable (`CLAUDE.md` §9).

---

## 6. Sondeo del flujo completo (Request → Response)

### 6.1 `vet` — READ (`GET /`)

```
Navegador → GET /
  → config/urls.py ('' → vet.urls)
  → vet/urls.py ('' → cita_list)
  → vet/views.py :: cita_list(request)
  → Cita.objects.order_by('fecha','hora')   [Manager → QuerySet]
  → Django ORM → SELECT * FROM vet_cita ORDER BY fecha, hora
  → SQLite
  → Context {'citas': …}
  → templates/vet/cita_list.html (extiende base.html)
  → HTML Response → Navegador
```

### 6.2 `vet` — CREATE (`POST /nueva/`)

```
Formulario → POST /nueva/ → cita_crear(request)
  → CitaForm(request.POST).is_valid()  →  clean() consulta Cita.objects.filter(...)
  → Cita.objects.create(**datos) → Django ORM → INSERT INTO vet_cita (...) → SQLite
  → redirect('vet:cita_list')   [Post/Redirect/Get]
  → vuelve a 6.1 y muestra la cita nueva
```

### 6.3 `biblioteca` — CRUD (ej. entidad `Libro`)

```
/biblioteca/libros/                → LibroListView   → SELECT → lista
/biblioteca/libros/nuevo/          → LibroCreateView → INSERT → redirect a la lista
/biblioteca/libros/<pk>/editar/    → LibroUpdateView → UPDATE → redirect a la lista
/biblioteca/libros/<pk>/eliminar/  → LibroDeleteView → confirmación → POST → DELETE → redirect
```

Equivalencia **ORM → SQL** (`GLAB-S03.md` Ej. 19, `INFORME_Lab03.md` Ej. 6):

| CRUD | Django ORM | SQL |
|---|---|---|
| CREATE | `Model.objects.create(...)` / `CreateView` | `INSERT` |
| READ | `Model.objects.all()` / `.order_by()` / `ListView` | `SELECT` |
| UPDATE | recuperar objeto → `save()` / `UpdateView` | `UPDATE` |
| DELETE | `objeto.delete()` / `DeleteView` | `DELETE` |

Todo mediante Django ORM, **sin SQL manual**.

---

## 7. Índice rápido de funciones y clases

| # | Elemento | Archivo | Tipo |
|---|---|---|---|
| 1 | `urlpatterns` | config/urls.py | Enrutado raíz |
| 2 | `Cita` | vet/models.py | Model |
| 3 | `Cita.__str__` | vet/models.py | Método |
| 4 | `CitaForm` | vet/forms.py | Form |
| 5 | `CitaForm.clean` | vet/forms.py | Validación |
| 6 | `cita_list` | vet/views.py | View (función) — READ |
| 7 | `cita_crear` | vet/views.py | View (función) — CREATE |
| 8 | `VetConfig` | vet/apps.py | AppConfig |
| 9 | `Migration` (Cita) | vet/migrations/0001_initial.py | Migración |
| 10 | `Bibliotecario` | biblioteca/models.py | Model independiente |
| 11 | `Editorial` | biblioteca/models.py | Model independiente |
| 12 | `Socio` | biblioteca/models.py | Model independiente |
| 13 | `Categoria` | biblioteca/models.py | Model (lado 1) |
| 14 | `Libro` | biblioteca/models.py | Model (lado N, FK) |
| 15–18 | `Bibliotecario{List,Create,Update,Delete}View` | biblioteca/views.py | CBV — CRUD |
| 19–22 | `Editorial{List,Create,Update,Delete}View` | biblioteca/views.py | CBV — CRUD |
| 23–26 | `Socio{List,Create,Update,Delete}View` | biblioteca/views.py | CBV — CRUD |
| 27–30 | `Categoria{List,Create,Update,Delete}View` | biblioteca/views.py | CBV — CRUD |
| 31–34 | `Libro{List,Create,Update,Delete}View` | biblioteca/views.py | CBV — CRUD |
| 35 | `urlpatterns` (20 rutas) | biblioteca/urls.py | Enrutado de App |
| 36 | `admin.site.register` ×5 | biblioteca/admin.py | Registro en Admin |
| 37 | `BibliotecaConfig` | biblioteca/apps.py | AppConfig |
| 38 | `Migration` (5 modelos) | biblioteca/migrations/0001_initial.py | Migración |
