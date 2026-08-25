# Sesión 02 — Arquitectura de Django: Project, App, MVT y el ciclo Request/Response

Contenido de la Semana 2 del curso **Desarrollo de Aplicaciones Empresariales**
(4 - C24 - Sección CD). Fuentes: `PPT-S02-YBESTARD-2026-02.pptx` (teoría) y
`GLAB-S02-YBESTARD-2026-02.docx` (laboratorio). Estudiante: **Renzo León**.

## Objetivo de la sesión

Construir el mapa completo de Django — Project, App, MVT, Request/Response — y
conectarlo con el proyecto real **DjangoInicial** (`config` / `core` / `Item`) del
Laboratorio 01 ([Semana 1](../Semana%201/CLAUDE.md)). Esta sesión es teórica: no se
crea código nuevo, se explica el que ya existe y se prepara el terreno para agregar
una nueva App (`store`) en la Presentación 2 / próximo laboratorio.

## Capacidades terminales

1. Identificar la estructura básica de un proyecto Django.
2. Diferenciar un Project de una App.
3. Explicar el patrón Model–View–Template (MVT).
4. Describir el flujo de una solicitud HTTP desde la URL hasta la respuesta.
5. Reconocer la función de Models, Views, URLs, Templates, ORM y migraciones.

## Contenido

1. Django y las aplicaciones web
2. Project y Apps
3. Estructura de Django
4. Arquitectura MVT
5. Request y Response
6. URLs y Views
7. Models y ORM
8. Migraciones
9. Templates y Context
10. Flujo completo de una aplicación

## 1. ¿Qué es Django?

Framework web de código abierto, escrito en Python, que ofrece estructura y
herramientas para resolver problemas comunes de desarrollo web (routing, models,
views, templates, forms, authentication, admin, ORM) evitando construir cada
componente desde cero.

## 2. Qué ocurre detrás de una aplicación web

Cuando un usuario abre una página, consulta datos o presiona un botón, el
navegador envía una **solicitud (Request)** al servidor y espera una **respuesta
(Response)**:

```
Usuario → Navegador → Request → Servidor → Aplicación → Base de datos
                                                ↓
Usuario ← Navegador ← Response ←───────────────┘
```

## 3. Project vs App

- **Project** = sistema completo (un único contenedor de configuración).
- **App** = módulo funcional que resuelve una responsabilidad concreta y puede
  reutilizarse en otros proyectos.
- Un Project puede contener varias Apps (ej. un Sistema Empresarial con `clientes`,
  `productos`, `ventas`, `inventario`).

**En el proyecto real (`django_project/src/`):**

```
django_project/src/
├── config/   → EL PROJECT (configuración)
└── core/     → UNA APP (modelo Item)
```

```powershell
django-admin startproject config .
python manage.py startapp core
```

Por ahora solo existe la App `core`; en la siguiente sesión se agrega `store`.

## 4. Arquitectura MVT (Model–View–Template)

Patrón arquitectónico de Django que separa tres responsabilidades: **datos**,
**procesamiento de la solicitud** y **presentación visual**.

| Componente | Rol |
|---|---|
| **Model** | Datos |
| **View** | Procesamiento — recibe la solicitud y decide qué hacer |
| **Template** | Presentación — genera la respuesta HTML |

Flujo: `Request → URL → View ↔ Model → Template → Response`

Ejemplo: un usuario visita `/productos/`; el Model `Product` provee los datos, la
View `product_list()` los consulta y decide qué hacer, y el Template
`product_list.html` los muestra como tabla HTML.

### MVT vs MVC

MVC (Model–View–Controller) es el patrón clásico y más general (ASP.NET, Laravel).
Django lo llama MVT porque redefine dos nombres:

| MVC | Django MVT |
|---|---|
| Model | Model |
| Controller | **View** |
| View | **Template** |

> Punto de confusión frecuente: la **View de Django** (procesamiento, similar a un
> Controller) no es la **View de MVC** (presentación) — ese rol en Django lo cumple
> el **Template**.

Ejemplo equivalente: `ProductController` (ASP.NET) ≈ `product_list(request)`
(Django View); `Products.cshtml` (ASP.NET View) ≈ `product_list.html` (Django
Template).

## 5. URLs

`urls.py` es el mecanismo de enrutamiento: recibe la ruta solicitada, la compara
contra patrones definidos con `path()` y delega el procesamiento a la View
correspondiente ("director de tráfico").

## 6. Views

Función (o clase) que recibe una solicitud HTTP, decide qué hacer —típicamente
consultando datos vía un Model— y devuelve una respuesta, casi siempre renderizando
un Template con esos datos.

```python
# core/urls.py
path("", views.item_list, name="item_list")

# core/views.py
def item_list(request):
    ...
```

URL = ¿a dónde va la solicitud? · View = ¿qué hacemos con la solicitud?

## 7. Models y ORM

Un **Model** es una clase de Python que representa una entidad de datos: cada
atributo se mapea a una columna de una tabla. Puede incluir validaciones,
relaciones y métodos propios.

El **ORM** (Object-Relational Mapping) traduce automáticamente operaciones sobre
objetos Python (instancias de un Model) en sentencias SQL, y viceversa.

```python
# core/models.py (código real)
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

`Item.objects.all()` → Django ORM → `SELECT * FROM item WHERE ...` → SQLite.

Comparación conceptual (no exacta): QuerySet de Django ≈ LINQ/Entity Framework en
.NET.

## 8. Migraciones

Archivos generados por Django que registran, de forma versionada, los cambios
realizados en los Models.

- `makemigrations` — crea los archivos a partir de las diferencias en `models.py`.
- `migrate` — los aplica a la base de datos real.

```powershell
python manage.py makemigrations core
python manage.py migrate
```

En el proyecto real: `core/migrations/0001_initial.py` crea la tabla del modelo
`Item`.

## 9. Templates y Context

Un **Template** es un archivo (normalmente HTML) que combina marcado estático con
marcadores dinámicos (`{{ variable }}`, `{% for %}`, `{% if %}`) y puede heredar de
otro con `{% extends %}`.

El **Context** es el diccionario que una View envía al Template al renderizarlo:
cada clave queda disponible como variable dentro del Template.

```python
# core/views.py
items = Item.objects.all()
return render(request, "core/item_list.html", {'items': items})
```

```html
<!-- core/templates/core/item_list.html -->
{% for item in items %}
    {{ item.name }}
{% endfor %}
```

Herencia real: `base.html` → `item_list.html`.

## 10. El proyecto vacío vs. el proyecto real

**Un proyecto Django recién creado** (`startproject`) ya trae:

| Archivo | Para qué sirve |
|---|---|
| `manage.py` | Herramienta de administración (`runserver`, `migrate`, `startapp`) |
| `settings.py` | `INSTALLED_APPS`, `MIDDLEWARE`, `DATABASES`, `TEMPLATES`, `STATIC_URL` |
| `urls.py` / `asgi.py` / `wsgi.py` | Entrada de rutas y de servidores |

Todavía **no** existen: Apps propias, Models propios, Views propias, Templates
propios, URLs de una App.

**El proyecto real DjangoInicial** (`config` / `core` / `Item`) ya implementa todo
eso — repositorio: `github.com/ybestard2021/DjangoInicial.git`.

```python
# config/settings.py
INSTALLED_APPS = [..., 'core']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
ROOT_URLCONF = 'config.urls'

# config/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
```

`/admin/` → Django Admin · `/` → `core.urls`

### Flujo real del proyecto DjangoInicial

```
Usuario → GET / → config/urls.py → core/urls.py → core/views.py → item_list()
    → Item.objects.all() → Django ORM → SQLite
    → Context → item_list.html (extiende base.html) → HTML Response → Navegador
```

### Flujo de ejecución vs. flujo de desarrollo

No es lo mismo cómo **funciona** Django en cada solicitud que cómo se **construye**
paso a paso una app Django:

| Flujo de ejecución (cada request) | Flujo de desarrollo (una vez, por el programador) |
|---|---|
| Request → URL → View → Model → Template → Response | venv → startproject → startapp → models → makemigrations → migrate → views → urls → templates → runserver |

## Conclusiones de la sesión

- Django organiza una aplicación mediante Projects y Apps.
- MVT separa datos, procesamiento y presentación.
- Una solicitud recorre URL → View → Model → Template → Response.
- Django ORM permite trabajar con la base de datos usando objetos Python.
- Las migraciones aplican los cambios de los Models a la base de datos.
- El proyecto DjangoInicial (`config`/`core`/`Item`) implementa exactamente este flujo.

## Preguntas de comprobación

| Pregunta | Respuesta |
|---|---|
| ¿Qué componente determina qué View se ejecuta? | `urls.py` |
| ¿Dónde se definen las entidades de datos? | `models.py` |
| ¿Qué comando aplica las migraciones? | `migrate` |
| ¿Qué componente genera el HTML final? | Template |
| ¿Qué componente cumple un papel similar al Controller de MVC? | View |

## Cómo vamos a trabajar hoy

- Repasar la teoría de arriba **sobre el proyecto ya existente** en
  [Semana 1](../Semana%201/CLAUDE.md) (`django_project/src/`), recorriendo
  `config` → `core` (urls, views, models, admin, templates) con el vocabulario
  MVT.
- El laboratorio de esta semana (nueva App con datos estáticos y formulario)
  está documentado aparte en [GLAB-S02.md](GLAB-S02.md).
- Referencia rápida de comandos, si hace falta relanzar el proyecto real:

```powershell
cd "D:\DAE\RenzoLeon\Semana 1\django_project\src"
..\venv\Scripts\python.exe manage.py runserver
```

  - Catálogo: http://127.0.0.1:8000/
  - Administración: http://127.0.0.1:8000/admin/

## Referencias bibliográficas

- Django Software Foundation. *Django documentation* — Version 5.2.
  docs.djangoproject.com/en/5.2/
- Django Software Foundation. *Writing your first Django app*.
  docs.djangoproject.com/en/5.2/intro/tutorial01/
- Django Software Foundation. *Models and databases*.
  docs.djangoproject.com/en/5.2/topics/db/
- Django Software Foundation. *URL dispatcher*.
  docs.djangoproject.com/en/5.2/topics/http/urls/
- Django Software Foundation. *Templates*.
  docs.djangoproject.com/en/5.2/topics/templates/
- Repositorio del ejemplo: github.com/ybestard2021/DjangoInicial.git
