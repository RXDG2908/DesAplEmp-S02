# Tema 2 — Arquitectura MVT, URLs, Views, Templates y Forms (Semana 2)

## Qué ocurre detrás de una app web

```
Usuario → Navegador → Request → Servidor → Aplicación → Base de datos
                                                ↓
Usuario ← Navegador ← Response ←───────────────┘
```

## Project vs App

- **Project** = sistema completo (contenedor de configuración).
- **App** = módulo funcional, reutilizable.
- `django_project/src/`: `config/` = Project, `core/` = App.

## Arquitectura MVT (Model–View–Template)

| Componente | Rol |
|---|---|
| **Model** | Datos |
| **View** | Procesamiento — recibe la solicitud y decide qué hacer |
| **Template** | Presentación — genera el HTML |

Flujo: `Request → URL → View ↔ Model → Template → Response`

### MVT vs MVC

| MVC | Django MVT |
|---|---|
| Model | Model |
| Controller | **View** |
| View | **Template** |

La View de Django (procesamiento) ≈ Controller de MVC. El Template de Django
(presentación HTML) ≈ View de MVC. Son nombres distintos para roles distintos
de los que uno esperaría por analogía directa.

## URLs

`urls.py` = mecanismo de enrutamiento. Compara la ruta solicitada contra
patrones `path()` y delega a la View correspondiente.

```python
# core/urls.py
path("", views.item_list, name="item_list")
```

## Views

Función (o clase) que recibe una solicitud HTTP, decide qué hacer (consultando
un Model) y devuelve una respuesta, normalmente renderizando un Template.

```python
def item_list(request):
    items = Item.objects.all()
    return render(request, "core/item_list.html", {'items': items})
```

URL = ¿a dónde va la solicitud? · View = ¿qué hacemos con la solicitud?

## Models (repaso, se profundiza en el Tema 3)

Clase Python que representa una entidad: cada atributo = una columna.

```python
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Templates y Context

**Template:** archivo (HTML) con marcado estático + marcadores dinámicos
(`{{ variable }}`, `{% for %}`, `{% if %}`). Herencia con `{% extends %}`.

**Context:** diccionario que la View envía al Template al renderizar; cada
clave queda disponible como variable.

```python
items = Item.objects.all()
return render(request, "core/item_list.html", {'items': items})
```

```html
{% for item in items %}
    {{ item.name }}
{% empty %}
    No hay items registrados.
{% endfor %}
```

Herencia real: `base.html` → `item_list.html`.

## Forms (Laboratorio 2 — App propia sin base de datos)

En el Laboratorio 2 se creó una App nueva (`vet`, `biblioteca`, etc.) sobre
una problemática propia, **sin base de datos todavía**: los datos vivían como
lista de diccionarios en `models.py`, y el formulario usaba `forms.Form` (NO
`ModelForm`, porque no había Model persistente).

```python
class CitaForm(forms.Form):
    mascota = forms.CharField(max_length=100)
    dueno = forms.CharField(max_length=100)
    servicio = forms.ChoiceField(choices=Cita.SERVICIOS)
    fecha = forms.DateField()
    hora = forms.TimeField()
```

Flujo de creación: Formulario → `POST` → `request.POST` → View valida
(`form.is_valid()`) → agrega a la lista en memoria → redirige al listado.

**Importante:** en este punto los datos se perdían al reiniciar el servidor
(no había persistencia). Eso se resuelve recién en la Semana 3.

## Flujo real del proyecto (con Model persistente, Semana 1→2)

```
Usuario → GET / → config/urls.py → core/urls.py → core/views.py → item_list()
    → Item.objects.all() → Django ORM → SQLite
    → Context → item_list.html (extiende base.html) → HTML Response → Navegador
```

## Flujo de ejecución vs. flujo de desarrollo

| Flujo de ejecución (cada request) | Flujo de desarrollo (una vez) |
|---|---|
| Request → URL → View → Model → Template → Response | venv → startproject → startapp → models → makemigrations → migrate → views → urls → templates → runserver |
