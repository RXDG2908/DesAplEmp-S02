# Pendiente Laboratorio 5 — para Lucas Inga

Hola. Este es un mensaje para el Claude que está ayudando a **Lucas Inga** en
este mismo repositorio (`RXDG2908/DesAplEmp-S02`). El laboratorio es grupal
(Lucas Inga - Renzo León) y **Renzo ya resolvió la Parte 1** (app `vet`).
Este documento explica exactamente qué falta: la **Parte 2**, sobre la app
`biblioteca`.

## Contexto que ya está resuelto (no lo repitas)

- La Parte 1 del Laboratorio 5 (Ejercicios 1-8, sobre `vet`) está completa:
  ver [INFORME_Lab05.md](INFORME_Lab05.md) y `django_project/src/vet/admin.py`.
- Puedes usar `vet/admin.py` como plantilla de estilo: usa
  `admin.site.register(Modelo, ModeloAdmin)`, clases `ModelAdmin` con
  `list_display` / `search_fields` / `list_filter`, y clases
  `admin.StackedInline` / `admin.TabularInline` para las relaciones. No hay
  nada más sofisticado que eso — el curso no ha visto `@admin.register(...)`
  como decorador, `readonly_fields`, `fieldsets`, `autocomplete_fields`, ni
  nada de eso, así que **no los uses**. Mantente en las herramientas exactas
  que pide la guía.

## Qué falta: PARTE 2 — app `biblioteca` (investigación propia)

Archivo a editar: `django_project/src/biblioteca/admin.py`.

Estado actual de ese archivo (punto de partida):

```python
from django.contrib import admin

from .models import Bibliotecario, Categoria, Editorial, Libro, Socio

admin.site.register(Bibliotecario)
admin.site.register(Editorial)
admin.site.register(Socio)
admin.site.register(Categoria)
admin.site.register(Libro)
```

Ya están registradas 5 entidades, pero **sin personalizar** (registro
simple) y **faltan 2 entidades** de la Semana 4: `CarnetSocio` (relación
1:1 con `Socio`) y `Prestamo` (modelo intermedio `through` de la relación
N:M entre `Socio` y `Libro`). Con esas dos se llega a las **7 entidades**
que pide el checklist de la Parte 2.

Revisa `biblioteca/models.py` para confirmar los campos exactos de cada
modelo antes de escribir el `admin.py` (nombres de campos, relaciones,
`related_name`).

### Ejercicio 9 — Registrar las siete entidades en el Admin

Agrega el registro de `CarnetSocio` y `Prestamo`. **Importante:** igual que
se hizo en `vet` con `FichaClinica` y `ConsumoInsumo`, estas dos entidades
tienen sentido dentro de la pantalla de `Socio` (o de `Libro`), no como
listados sueltos — por eso lo correcto es exponerlas como **Inlines**
(Ejercicios 11 y 12), no con `admin.site.register()` aparte. Aun así, el
Ejercicio 9 pide verificar que las 7 cuentan como registradas: cuando
aparecen dentro de un Inline, ya están "registradas" a efectos del Admin
(se administran desde ahí). Documenta ese razonamiento en tu respuesta.

### Checklist obligatorio antes de continuar — Parte 2

Verifica cada punto con una captura antes de avanzar a los Ejercicios 10-14:

| # | Criterio | Cómo lo cumples |
|---|---|---|
| 1 | Las 7 entidades (5 originales + 1:1 + intermedio N:M) están en el Admin | Conteo directo en `admin.py` (registradas directamente o vía Inline) |
| 2 | ≥3 modelos usan una clase `ModelAdmin` (no solo `register()` sin personalizar) | Ver Ejercicio 10 |
| 3 | ≥2 modelos con `list_display` mostrando campos relevantes, no solo `__str__` | Ver Ejercicio 10 |
| 4 | ≥1 modelo con `search_fields` funcionando | Ver Ejercicio 10 |
| 5 | ≥1 modelo con `list_filter` funcionando | Ver Ejercicio 10 |
| 6 | La relación `OneToOneField` (`CarnetSocio`) expuesta con `StackedInline` | Ver Ejercicio 11 |
| 7 | El modelo intermedio N:M (`Prestamo`) expuesto con `TabularInline` | Ver Ejercicio 12 |
| 8 | ≥1 operación completa de creación, edición y eliminación desde el Admin | Ver Ejercicio 13 |
| 9 | Explicación escrita de qué resuelve el Admin y qué seguiría necesitando View/Template propio | Ver Ejercicio 13 |

### Ejercicio 10 — Personalizar `ModelAdmin`

Elige ≥3 de las 7 entidades y dales una clase `ModelAdmin` (mismo patrón que
`CitaAdmin`/`VeterinarioAdmin` en `vet/admin.py`). Sugerencia razonable según
los campos de `biblioteca/models.py`:

- `LibroAdmin`: `list_display` con título, autor, categoría, año;
  `search_fields` sobre título/autor/ISBN.
- `SocioAdmin`: `list_display` con nombre, DNI, teléfono; `search_fields`
  sobre nombre/DNI.
- `PrestamoAdmin` (si decides registrarlo también aparte, además de
  Inline): `list_filter` sobre `estado`.

Usa `list_filter` en al menos un modelo con un campo que tenga sentido
filtrar (por ejemplo `estado` en `Prestamo`, o `categoria` en `Libro`).

### Ejercicio 11 — `StackedInline` para la relación 1:1

```python
class CarnetSocioInline(admin.StackedInline):
    model = CarnetSocio
    extra = 0
```

Agrégalo a `SocioAdmin.inlines` para que el carnet se vea y edite dentro de
la misma pantalla del Socio.

### Ejercicio 12 — `TabularInline` para el modelo intermedio N:M

```python
class PrestamoInline(admin.TabularInline):
    model = Prestamo
    extra = 1
```

Agrégalo a `SocioAdmin.inlines` (o a `LibroAdmin.inlines`, elige el lado que
tenga más sentido para tu justificación) mostrando como columnas los
atributos propios de `Prestamo` (fechas, estado).

### Ejercicio 13 — Verificar el flujo completo

Desde el panel del Admin: crea, edita y elimina al menos un registro
relacionado (usando los Inlines). Documenta con capturas antes/después y
confirma que persiste en `db.sqlite3`. Luego escribe el párrafo pedido: qué
resuelve el Admin para esta investigación (biblioteca) y qué seguiría
necesitando una View y un Template propios (por ejemplo, una pantalla
pública donde un socio consulte sus propios préstamos, que el Admin no
ofrece porque es solo para staff).

### Ejercicio 14 — Publicar en GitHub

Actualiza `requirements.txt` y `README.md` describiendo qué quedó registrado
y personalizado en el Admin de `biblioteca`. Haz commit y push. Incluye la
URL del repositorio en el documento de entrega si tu parte lo requiere (el
repo ya es el mismo que usa Renzo: `https://github.com/RXDG2908/DesAplEmp-S02`).

## Recordatorio de alcance

No introduzcas nada fuera de lo visto en las Semanas 1-4 y en la propia guía
de la Semana 5: sin `@admin.register`, sin `readonly_fields`, sin
`fieldsets`, sin `autocomplete_fields`, sin JavaScript/CSS personalizado en
el Admin, sin apps de terceros (`django-import-export`, etc.). Todo se
resuelve con `admin.site.register()`, `ModelAdmin` (`list_display`,
`search_fields`, `list_filter`) y las dos clases Inline
(`StackedInline`, `TabularInline`), tal como en `vet/admin.py`.
