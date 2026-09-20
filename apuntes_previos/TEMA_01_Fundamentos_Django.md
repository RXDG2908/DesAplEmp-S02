# Tema 1 — Fundamentos de Django (Semana 1)

## ¿Qué es Django?

Framework web de código abierto, escrito en Python, gratuito. Provee un conjunto
de componentes para no reinventar la rueda al construir un sitio: routing,
Models, Views, Templates, Forms, Authentication, Admin, ORM.

**Qué hace Django:**
- Estructura de trabajo bajo el patrón **Model–Template–View (MVT)**.
- Mapea objetos Python con la base de datos mediante el **ORM**.
- URLs amigables para buscadores.
- Interfaz de administración automática (**Django Admin** — tema central de la
  Semana 5).
- Framework para manejar formularios.

## Organización de un proyecto Django

- Un desarrollo es un **Project**.
- Un Project consta de una o varias **Apps**.
- Cada App resuelve algo concreto y puede reutilizarse en otros proyectos.
- Ejemplo: Project "Sistema Empresarial" → Apps `clientes`, `productos`,
  `ventas`, `inventario`.

## Entorno de trabajo

```powershell
python -m venv venv
venv\Scripts\activate
pip install django
python -m django --version
```

El entorno virtual aísla la configuración Python/Django por proyecto: cambios
en un proyecto no afectan a otros.

## Crear el primer proyecto

```powershell
django-admin startproject config .
```

Estructura generada:

```
src/
├── manage.py
└── config/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

En un proyecto recién creado **todavía no existen**: Apps propias, Models
propios, Views propias, Templates propios, URLs de una App.

## Levantar el servidor

```powershell
python manage.py runserver
python manage.py runserver 8080   # cambiar de puerto
```

`http://127.0.0.1:8000/`

## En el proyecto real (`django_project/src/`)

```
django_project/src/
├── config/   → EL PROJECT (configuración)
└── core/     → UNA APP (modelo Item, Semana 1)
```

```powershell
django-admin startproject config .
python manage.py startapp core
```

Laboratorio 1: se creó la App `core` con el modelo `Item` (`name`,
`description`, `created_at`), su View de listado, URLs, templates
(`base.html` → `item_list.html`) y se registró en el Django Admin por primera
vez (`admin.site.register(Item)`, `createsuperuser`) — ese registro simple es
el punto de partida que la Semana 5 va a personalizar y ampliar con
`ModelAdmin` e Inlines.

## Conclusión clave para la Semana 5

Django Admin no es un tema nuevo desde cero: `admin.site.register()` ya se
usó en el Laboratorio 1 para exponer `Item`. La Semana 5 retoma exactamente
ese mecanismo y lo profundiza.
