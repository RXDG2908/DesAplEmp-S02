# Exposición — Laboratorio 06, Parte 1: Motor de plantillas de Django en la app `vet`

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** revisar y refactorizar los templates de la app `vet` usando las
herramientas del motor de plantillas: herencia, filtros, comentarios,
`include` y escape automático.

> Este documento explica, en el orden en que se hicieron, los ocho
> ejercicios de la Parte 1 del Laboratorio 6. La Parte 2 (templates de
> `biblioteca`) corresponde a Lucas Inga.

---

## Conceptos clave (lectura rápida)

- **Motor de plantillas:** la parte de Django que convierte un **Template + Context** en el **HTML final**.
- **Herencia de plantillas:** una plantilla **base** define la estructura común (encabezado, menú, pie) y deja **huecos**; las **hijas** solo llenan esos huecos.
  - **`{% extends 'base.html' %}`** → indica de qué plantilla **hereda** (debe ser la **primera etiqueta**).
  - **`{% block content %}...{% endblock %}`** → el **hueco** que la hija rellena.
  - Ventaja: cambiar el menú o el pie se hace **en un solo archivo**.
- **Variables `{{ }}`:** muestran un dato del Context.
- **Etiquetas `{% %}`:** lógica: `for`, `if`, `url`, `include`, `csrf_token`.
- **Filtros (`|`):** dan **formato** sin tocar la View:
  - **`date`/`time`** → formato de fecha y hora.
  - **`floatformat:2`** → **dos decimales** (precios).
  - **`title`** → **Mayúscula Inicial** en cada palabra.
  - **`default`** → texto si el dato **falta**.
  - **`length`** → **cuenta** elementos.
- **Comentarios `{# #}`:** **no llegan al HTML** final (a diferencia de `<!-- -->`); solo una línea.
- **`{% include %}`:** inserta un **fragmento reutilizable** (`_veterinario_info.html`); se edita **una sola vez**.
- **Escape automático (auto-escape):** todo lo que va en `{{ }}` se **convierte en texto seguro** (`<` → `&lt;`); un `script` escrito por un usuario **no se ejecuta** (protección **XSS**). El filtro **`safe`** lo desactiva.

---

## De dónde partimos

Para la Semana 6, `vet` ya tenía tres pantallas propias: el listado de
citas, el formulario de nueva cita y el detalle de una cita con sus tres
relaciones. En la Semana 5 se había visto el Django Admin, que resuelve el
CRUD sin escribir templates.

La idea central del laboratorio es que **no se crean pantallas nuevas**: las
rutas, las vistas y los modelos no cambian. Todo el trabajo está en los
templates, para que sean más fáciles de mantener, se lean mejor y sigan
siendo seguros. Y la pregunta de fondo: ¿qué ganan estas pantallas propias
frente al Admin?

---

## Paso 1 — Auditar los templates actuales (Ejercicio 1)

**Ver en el código:** [cita_list.html (L3)](django_project/src/templates/vet/cita_list.html#L3) · [cita_form.html (L3)](django_project/src/templates/vet/cita_form.html#L3) · [cita_detalle.html (L3)](django_project/src/templates/vet/cita_detalle.html#L3)

Se revisaron las tres plantillas de `vet`: `cita_list.html`,
`cita_form.html` y `cita_detalle.html`. Las tres ya heredaban de
`base.html` desde semanas anteriores, así que no había ninguna escrita "a
mano" de principio a fin que hubiera que migrar desde cero.

---

## Paso 2 — La plantilla base (Ejercicio 2)

**Ver en el código:** [templates/base.html — `block title` (L6)](django_project/src/templates/base.html#L6) · [`<nav>` (L38)](django_project/src/templates/base.html#L38) · [`block content` (L52)](django_project/src/templates/base.html#L52) · [`<footer>` (L56)](django_project/src/templates/base.html#L56)

`templates/base.html` ya existía. Tiene:

- el encabezado con el título,
- el menú de navegación (citas, libros, socios, préstamos, carnets),
- un pie de página,
- y el bloque vacío `{% block content %}{% endblock %}`, donde cada
  plantilla hija pone lo suyo (más `{% block title %}` para el título de la
  pestaña).

En este laboratorio solo se cambió el texto del pie para que diga
Laboratorio 06.

---

## Paso 3 y 4 — Herencia en todos los templates (Ejercicios 3 y 4)

**Ver en el código:** [cita_list.html — `extends` / `block` (L3)](django_project/src/templates/vet/cita_list.html#L3) · [cita_form.html (L3)](django_project/src/templates/vet/cita_form.html#L3) · [cita_detalle.html (L3)](django_project/src/templates/vet/cita_detalle.html#L3)

El listado empieza con `{% extends 'base.html' %}` y define únicamente su
contenido dentro de `{% block content %}`. La vista que lo muestra no se
tocó, y la página sigue mostrando los mismos datos.

El formulario y el detalle hacen lo mismo. Resultado: las tres pantallas de
`vet` comparten el mismo encabezado, menú y pie, y si mañana cambia el menú
se edita **en un solo archivo**.

---

## Paso 5 — Aplicar filtros (Ejercicio 5)

**Ver en el código:** [cita_detalle.html — `floatformat:2` (L41)](django_project/src/templates/vet/cita_detalle.html#L41) · [total (L49)](django_project/src/templates/vet/cita_detalle.html#L49) · [cita_list.html — `title` (L32)](django_project/src/templates/vet/cita_list.html#L32)

Ya se usaban filtros desde antes: `date:"d/m/Y"` y `time:"H:i"` para fechas
y horas, `length` para contar las citas del listado y `default` para
mostrar un texto cuando falta un dato. En este laboratorio se agregaron dos:

```django
<td>S/ {{ consumo.precio_unitario|floatformat:2 }}</td>   {# cita_detalle.html #}
<td>{{ cita.mascota|title }}</td>                           {# cita_list.html #}
```

- `floatformat:2`: precios, subtotales y total de insumos siempre con dos
  decimales, con formato de precio.
- `title`: el nombre de la mascota con la primera letra de cada palabra en
  mayúscula.

Los filtros dan formato **en la presentación**, sin tocar las vistas ni los
datos guardados.

---

## Paso 6 — Documentar con comentarios (Ejercicio 6)

**Ver en el código:** [cita_detalle.html — comentarios (L12)](django_project/src/templates/vet/cita_detalle.html#L12) · [cita_list.html — comentario `select_related` (L38)](django_project/src/templates/vet/cita_list.html#L38)

Se usaron comentarios de plantilla `{# ... #}`, que **no llegan al HTML
final** (a diferencia de `<!-- -->`, que el usuario sí puede ver en el
código fuente). Por ejemplo, en `cita_detalle.html` hay uno antes de cada
relación:

```django
{# 1) ACCESO DIRECTO a la FK (1:N): objeto.relacionado #}
{# 2) ACCESO INVERSO al 1:1 mediante el related_name 'ficha' #}
{# 3) RECORRIDO DEL MODELO INTERMEDIO: cita -> consumos -> insumo #}
```

y en el listado uno que aclara que el veterinario se obtiene sin consultas
extra gracias a `select_related`.

---

## Paso 7 — Reutilizar con `include` (Ejercicio 7)

**Ver en el código:** [templates/vet/_veterinario_info.html (L3)](django_project/src/templates/vet/_veterinario_info.html#L3) · [include en cita_list.html (L39)](django_project/src/templates/vet/cita_list.html#L39) · [include en cita_detalle.html (L14)](django_project/src/templates/vet/cita_detalle.html#L14)

El nombre del veterinario con su especialidad se mostraba igual en el
listado y en el detalle. Ese fragmento se sacó a un archivo propio,
`templates/vet/_veterinario_info.html`:

```django
{{ cita.veterinario.nombre|default:"Sin asignar" }}{% if cita.veterinario.especialidad %} ({{ cita.veterinario.especialidad }}){% endif %}
```

y ambas plantillas lo insertan con:

```django
{% include "vet/_veterinario_info.html" %}
```

El guion bajo inicial indica que es un fragmento, no una página completa. Si
cambia cómo se muestra el veterinario, se edita en un solo lugar.

---

## Paso 8 — Seguridad y comparación con el Admin (Ejercicio 8)

**Ver en el código:** [cita_list.html — datos con `{{ }}` (L32)](django_project/src/templates/vet/cita_list.html#L32)

**Prueba de escape automático:** se registró una cita con la mascota
escrita como `<script>...</script>` y el dueño con etiquetas `<b>`. Al abrir
el listado, el texto se ve tal cual, como letras; el código fuente muestra
`&lt;` y `&gt;` en lugar de `<` y `>`, y el script **nunca se ejecutó**.
Django escapa automáticamente todo lo que se muestra con `{{ }}`, y ninguna
plantilla usa el filtro `safe`, que desactivaría esa protección.

**Frente al Admin:** el Admin es una herramienta interna para el personal,
que entra con usuario y contraseña. Las plantillas propias son las páginas
públicas que ve el cliente: con el diseño de la clínica, sus propias
direcciones y los datos ordenados como conviene, con una estructura común
que se cambia en un solo sitio y el escape automático protegiendo cada
campo.

---

## Cómo se verificó cada paso (resumen de pruebas)

| Paso | Qué se probó | Resultado |
|---|---|---|
| 3-4 | Listado, formulario y detalle muestran menú y pie de la base | Correcto |
| 4 | El detalle sigue mostrando las tres relaciones igual que antes | Correcto |
| 5 | Precios y subtotales siempre con dos decimales | Correcto |
| 7 | El veterinario se ve igual en listado y detalle (mismo fragmento) | Correcto |
| 8 | Una cita con `<script>` en el nombre se muestra como texto | Correcto |
| 8 | Una cita normal sigue apareciendo en el listado | Correcto |

---

## Conclusión de la Parte 1

El hilo conductor es que **ninguno de estos cambios se nota en lo que ve el
usuario, pero sí en el mantenimiento**: la herencia concentra la estructura
común en `base.html`, los filtros dan formato sin tocar las vistas, los
comentarios documentan sin ensuciar el HTML, y el `include` evita copiar y
pegar el mismo fragmento. Todo eso con el escape automático cuidando los
datos que escriben los usuarios. El Admin y las plantillas propias no
compiten: uno es para el personal, las otras para el cliente.
