# SÚPER ÍNDICE — App `vet` (Reserva de citas de veterinaria)

Todo lo que hay en la App `vet`: **dónde está cada cosa, cómo llegar al archivo y
qué hace**. Vocabulario del material del curso: patrón **MVT**
(Model–View–Template), ciclo **Request → Response**, **URLs y Views**, **Models y
ORM**, **migraciones**, **Templates y Context** ([CLAUDE.md](CLAUDE.md)), y el
**flujo CRUD** `Request → URL → View → Model → ORM → SQLite → Template → Response`
([GLAB-S03.md](GLAB-S03.md)).

La App `vet` nació en el **Laboratorio 02** con datos en memoria y en el
**Laboratorio 03 (Parte 1)** se pasó a **Django ORM + SQLite**.

---

## 0. Cómo llegar a la App

```
D:\DesAplEmp-S02\                 ← repositorio
└── django_project\
    └── src\                      ← acá se ejecuta manage.py
        ├── config\               ← EL PROJECT (configuración)
        ├── templates\
        │   ├── base.html
        │   └── vet\              ← plantillas de la App
        └── vet\                  ← LA APP  ⭐
```

Ruta completa de la App: `django_project/src/vet/`
Para correr el servidor: abrir una terminal **en `django_project/src/`** y ejecutar
`python manage.py runserver`.

---

## 1. Mapa de la App `vet` (archivo por archivo)

| Archivo | Rol en MVT | Qué contiene | Cómo llegar |
|---|---|---|---|
| [vet/models.py](django_project/src/vet/models.py) | **Model** (datos) | Clase `Cita` | `src/vet/models.py` |
| [vet/views.py](django_project/src/vet/views.py) | **View** (procesa el request) | `cita_list`, `cita_crear` | `src/vet/views.py` |
| [vet/forms.py](django_project/src/vet/forms.py) | Apoyo a la View | `CitaForm` (valida el formulario) | `src/vet/forms.py` |
| [vet/urls.py](django_project/src/vet/urls.py) | **URLs** (enrutado) | Rutas de la App | `src/vet/urls.py` |
| [vet/apps.py](django_project/src/vet/apps.py) | Config | `VetConfig` (registra la App) | `src/vet/apps.py` |
| [vet/admin.py](django_project/src/vet/admin.py) | Admin | Vacío (la App no usa el panel) | `src/vet/admin.py` |
| [vet/tests.py](django_project/src/vet/tests.py) | Pruebas | Plantilla vacía de `startapp` | `src/vet/tests.py` |
| [vet/migrations/0001_initial.py](django_project/src/vet/migrations/0001_initial.py) | **Migración** | Crea la tabla `vet_cita` | `src/vet/migrations/` |
| [vet/__init__.py](django_project/src/vet/__init__.py) | — | Marca la carpeta como paquete Python | `src/vet/__init__.py` |
| [templates/vet/cita_list.html](django_project/src/templates/vet/cita_list.html) | **Template** | Tabla de citas | `src/templates/vet/` |
| [templates/vet/cita_form.html](django_project/src/templates/vet/cita_form.html) | **Template** | Formulario de registro | `src/templates/vet/` |
| [templates/base.html](django_project/src/templates/base.html) | **Template** base | Layout común (`{% block %}`) | `src/templates/` |

**Fuera de la App pero necesarios para que funcione:**

| Archivo | Qué aporta a `vet` | Cómo llegar |
|---|---|---|
| [config/settings.py](django_project/src/config/settings.py) | `'vet'` en `INSTALLED_APPS`; `DATABASES` = SQLite; carpeta `templates/` | `src/config/settings.py` |
| [config/urls.py](django_project/src/config/urls.py) | `path('', include('vet.urls'))` → la raíz `/` la maneja `vet` | `src/config/urls.py` |
| `db.sqlite3` | Base de datos real (no se sube a Git; se regenera con `migrate`) | `src/db.sqlite3` |

---

## 2. Cómo funciona cada archivo

### 2.1 `vet/models.py` — el Model `Cita`
- Clase `Cita(models.Model)` → Django la mapea a la tabla **`vet_cita`**.
- Campos (cada uno = una columna): `mascota`, `dueno`, `servicio`, `fecha`,
  `hora`, `estado`. Django agrega solo `id` como clave primaria.
- `SERVICIOS` y `ESTADOS`: listas de opciones fijas usadas como `choices` del
  campo. **No son una tabla** porque son catálogos cerrados, no los da de alta el
  usuario y no tienen datos propios (justificación pedida por el profesor,
  `INFORME_Lab03.md` Ej. 2).
- `__str__`: texto con el que se muestra una cita en el shell y en el admin.
- **Cómo llegar:** `src/vet/models.py`.

### 2.2 `vet/views.py` — las dos Views
| Función | Qué hace | ORM → SQL |
|---|---|---|
| `cita_list(request)` | **READ**: pide las citas ordenadas por fecha y hora y las manda al template. | `Cita.objects.order_by('fecha','hora')` → `SELECT` |
| `cita_crear(request)` | **CREATE**: si el `POST` es válido, guarda la cita y redirige al listado. | `Cita.objects.create(...)` → `INSERT` |
- `render(request, template, context)` construye el response HTML.
- `redirect('vet:cita_list')` aplica **Post/Redirect/Get**: evita duplicar la
  cita si el usuario refresca.
- **Cómo llegar:** `src/vet/views.py`.

### 2.3 `vet/forms.py` — `CitaForm`
- Hereda de `forms.Form` (no `ModelForm`), como indica el material.
- Define los campos que ve el usuario; `servicio` toma sus opciones de
  `Cita.SERVICIOS` (una sola fuente).
- `clean()`: validación entre varios campos. Consulta la tabla con
  `Cita.objects.filter(fecha=…, hora=…)` y prohíbe dos citas en el mismo horario.
- **Cómo llegar:** `src/vet/forms.py`.

### 2.4 `vet/urls.py` — enrutado de la App
- `app_name = 'vet'` → namespace para escribir `vet:cita_list` / `vet:cita_crear`.
- `path('', views.cita_list, name='cita_list')` → `/`
- `path('nueva/', views.cita_crear, name='cita_crear')` → `/nueva/`
- **Cómo llegar:** `src/vet/urls.py`.

### 2.5 `vet/apps.py` — `VetConfig`
- `name = 'vet'` (igual a la carpeta), `verbose_name = 'Citas veterinaria'`,
  `default_auto_field = BigAutoField` (tipo del `id` automático).
- Se registra en `INSTALLED_APPS` de `config/settings.py`.
- **Cómo llegar:** `src/vet/apps.py`.

### 2.6 `vet/migrations/0001_initial.py`
- Una sola operación `CreateModel(name='Cita')` con los 6 campos + `id`.
- Se genera con `makemigrations` y se aplica con `migrate` (crea `vet_cita` en
  SQLite). Distinto del CRUD: la migración cambia la **estructura**, el CRUD
  cambia los **datos** (`INFORME_Lab03.md` Ej. 3 y 6).
- **Cómo llegar:** `src/vet/migrations/0001_initial.py`.

### 2.7 Templates (`src/templates/vet/`)
| Template | Lo usa | Context que recibe | Etiquetas clave |
|---|---|---|---|
| `cita_list.html` | `cita_list` | `{'citas': QuerySet}` | `{% for cita in citas %}`, `{% empty %}` |
| `cita_form.html` | `cita_crear` | `{'form': CitaForm}` | `{% csrf_token %}`, `{{ form.as_p }}` |
| `base.html` | ambos | — | `{% block title %}`, `{% block content %}`, `{% url %}` |
- Herencia: `cita_list.html` y `cita_form.html` hacen `{% extends 'base.html' %}`.
- **Cómo llegar:** `src/templates/vet/` y `src/templates/base.html`.

---

## 3. Recorrido de una Request (dónde mirar en orden)

### READ — abrir el listado (`GET /`)
```
1. config/urls.py    →  path('', include('vet.urls'))
2. vet/urls.py       →  path('', views.cita_list)
3. vet/views.py      →  cita_list(): Cita.objects.order_by('fecha','hora')
4. vet/models.py     →  modelo Cita  →  Django ORM  →  SELECT  →  SQLite
5. views.py          →  render(..., {'citas': citas})   (Context)
6. templates/vet/cita_list.html  (extiende base.html)   →  HTML
7. Response  →  navegador
```

### CREATE — registrar una cita (`POST /nueva/`)
```
1. config/urls.py  →  2. vet/urls.py  →  path('nueva/', views.cita_crear)
3. vet/views.py    →  cita_crear(): CitaForm(request.POST).is_valid()
4. vet/forms.py    →  clean(): Cita.objects.filter(fecha, hora)  (ORM)
5. vet/views.py    →  Cita.objects.create(...)  →  ORM  →  INSERT  →  SQLite
6. redirect('vet:cita_list')   (Post/Redirect/Get)  →  vuelve al READ
```

### Equivalencia ORM → SQL
| Acción en la App | Django ORM | SQL |
|---|---|---|
| Ver el listado | `Cita.objects.order_by('fecha','hora')` | `SELECT * FROM vet_cita ORDER BY fecha, hora` |
| Registrar una cita | `Cita.objects.create(**datos)` | `INSERT INTO vet_cita (...) VALUES (...)` |
| Validar horario libre | `Cita.objects.filter(fecha=?, hora=?)` | `SELECT * FROM vet_cita WHERE fecha=? AND hora=?` |

---

## 4. Rutas de la App (URLs que se pueden abrir en el navegador)

| URL | View | Método | Qué pasa |
|---|---|---|---|
| `http://127.0.0.1:8000/` | `cita_list` | GET | Lista todas las citas (tabla). |
| `http://127.0.0.1:8000/nueva/` | `cita_crear` | GET | Muestra el formulario vacío. |
| `http://127.0.0.1:8000/nueva/` | `cita_crear` | POST | Valida, guarda y redirige a `/`. |
| `http://127.0.0.1:8000/admin/` | Django Admin | GET | Panel de admin (la App `vet` no registra modelos ahí). |

---

## 5. Comandos útiles (desde `django_project/src/`)

```powershell
python manage.py runserver          # levantar el servidor
python manage.py makemigrations     # generar migraciones si cambia models.py
python manage.py migrate            # crear/actualizar las tablas
python manage.py showmigrations     # ver qué migraciones están aplicadas
python manage.py sqlmigrate vet 0001   # ver el SQL de la migración
python manage.py shell              # consola para probar el ORM (Cita.objects.all())
```

---

# PREGUNTAS QUE PUEDE HACER EL PROFESOR

### Sobre estructura (Project / App)
1. **¿Cuál es el Project y cuál la App?** → Project: `config/`. App: `vet/`.
2. **¿Dónde se registra la App?** → En `INSTALLED_APPS` de `config/settings.py` (`'vet'`).
3. **¿Cómo llega una petición a `/` hasta la App `vet`?** → `config/urls.py` hace
   `path('', include('vet.urls'))` y `vet/urls.py` la manda a `cita_list`.
4. **¿Para qué sirve `app_name = 'vet'`?** → Namespace: permite `vet:cita_list`
   en templates y `redirect()` sin chocar con otras Apps.

### Sobre MVT
5. **¿Qué archivo cumple el rol de "Controller" de MVC?** → La **View**
   (`vet/views.py`).
6. **¿Qué genera el HTML final?** → El **Template** (`templates/vet/*.html`).
7. **¿Qué es el Context?** → El diccionario que la View pasa al Template
   (`{'citas': citas}` / `{'form': form}`).
8. **¿Dónde se define la entidad de datos?** → En `vet/models.py`, clase `Cita`.

### Sobre Models y ORM
9. **¿A qué tabla se mapea `Cita`?** → `vet_cita`.
10. **¿Qué campo agrega Django solo?** → `id` (clave primaria autoincremental).
11. **¿Por qué `SERVICIOS` y `ESTADOS` no son una tabla?** → Son catálogos
    cerrados, no los administra el usuario, no cambian en ejecución y no tienen
    datos propios; por eso van como `choices`. Si hubiera que gestionarlos se
    pasarían a un modelo `Servicio` con `ForeignKey`.
12. **¿Cómo consulta la View los datos?** →
    `Cita.objects.order_by('fecha','hora')` (Manager → QuerySet → ORM → SELECT).
13. **¿Cómo se guarda una cita nueva?** → `Cita.objects.create(...)` (ORM → INSERT).
14. **¿Qué SQL representa cada operación?** → ver la tabla del punto 3.
15. **¿Cómo probar el ORM sin navegador?** → `python manage.py shell` y
    `Cita.objects.all()` / `Cita.objects.count()`.

### Sobre migraciones
16. **¿Qué hace `makemigrations` y qué hace `migrate`?** → `makemigrations` crea
    el archivo con los cambios del modelo; `migrate` los aplica a SQLite.
17. **¿Qué archivo crea la tabla?** → `vet/migrations/0001_initial.py`
    (`CreateModel` de `Cita`).
18. **¿Diferencia entre migración y CRUD?** → La migración cambia la
    **estructura** de la base; el CRUD cambia los **datos**.
19. **¿Por qué `db.sqlite3` no está en el repo?** → Está en `.gitignore`; cada
    quien la regenera con `migrate`.

### Sobre Views, Forms y el flujo
20. **¿Qué pasa si el formulario no es válido?** → La View no guarda nada y
    vuelve a mostrar `cita_form.html` con los errores.
21. **¿Qué es Post/Redirect/Get y por qué se usa?** → Tras un `POST` válido se
    hace `redirect` al listado; así, si el usuario refresca, no se reenvía el
    `POST` ni se duplica la cita.
22. **¿Dónde está la validación de "no dos citas a la misma hora"?** → En
    `CitaForm.clean()` (`vet/forms.py`), con `Cita.objects.filter(...)`.
23. **¿Por qué `forms.Form` y no `ModelForm`?** → Porque así lo indica el
    material de la semana y deja explícito qué datos se piden.
24. **¿Para qué es `{% csrf_token %}` en el formulario?** → Protección de Django
    obligatoria en los formularios `POST`.

### Sobre la Semana 2 vs Semana 3
25. **¿Qué cambió respecto de la Semana 2?** → Antes `Cita` era una clase normal
    y los datos vivían en una lista en memoria; ahora hereda de `models.Model` y
    se guarda en SQLite con el ORM.
26. **¿Qué pasaba al reiniciar el servidor en la Semana 2?** → Se perdían todas
    las citas agregadas; la lista volvía a sus valores iniciales.
27. **¿Y ahora?** → Las citas persisten: siguen ahí después de reiniciar.
28. **¿Cambió el Template al pasar a base de datos?** → No; sigue recorriendo
    `citas`, solo que ahora vienen de SQLite y no de la memoria.
