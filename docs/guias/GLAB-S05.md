# GLAB-S05 — Guía de Laboratorio 05 (Semana 5)

**Curso:** Desarrollo de Aplicaciones Empresariales
**Carrera:** Desarrollo de Software
**Estudiante:** Bestard Aroche, Yunior
**Sección:** 4 - C24 - Sección CD
**Tema:** Administrador de Django (Django Admin) — registro de modelos relacionados, `ModelAdmin` e Inlines

> Fuente: `GLAB-S05-YBESTARD-2026-02.docx` (extracción de la información relevante para el desarrollo).

---

## Capacidades

- Identificar la funcionalidad del administrador de Django y su papel dentro de una aplicación empresarial.
- Registrar en el Django Admin modelos relacionados (1:1, 1:N y N:M) mediante `ModelAdmin`, personalizando `list_display`, `search_fields` y `list_filter`.
- Implementar el administrador y personalizar su plantilla en una aplicación Web en Django mediante Inlines (`TabularInline` y `StackedInline`) para exponer relaciones desde una sola pantalla.

## Seguridad

- Está prohibida la manipulación del hardware, conexiones eléctricas o de red, así como la ingesta de alimentos y bebidas.
- Ubicar maletines y/o mochilas en el lugar destinado para tal fin.
- Dejar la mesa de trabajo y la silla utilizada limpias y ordenadas.

## Fundamento teórico

- Revisar el material de la Semana 5 (Administrador de Django: registro de modelos, `ModelAdmin`, personalización y relaciones mediante Inlines) antes del desarrollo del laboratorio.

## Normas empleadas

- No aplica.

## Recursos

- Cada estudiante trabaja con una computadora con **Windows 11**.
- Los softwares requeridos ya están instalados en los laboratorios.
- Se requiere **Python 3.10 o superior**, **Django 5**, un editor de código (**Visual Studio Code**) y una **cuenta de GitHub** para el control de versiones.
- La aplicación desarrollada en el laboratorio de la **Semana 4** (Models con `OneToOneField`, `ForeignKey` y `ManyToManyField` con `through`) y, cuando corresponda, la investigación propia ampliada en la Parte 2 de dicho laboratorio.

## Metodología

- El desarrollo del laboratorio es **individual**.

## Modo de entrega

- Se entrega mediante el mismo documento Word, completando cada ejercicio con su respuesta y justificación.
- Cada ejercicio que lo requiera debe incluir **captura de pantalla del código en `admin.py`** y del **panel del Django Admin** en el navegador, mostrando explícitamente el registro de modelos, la personalización (`list_display`, `search_fields`, `list_filter`) y los Inlines implementados.
- El documento debe incluir la URL del repositorio de GitHub donde se aloja el proyecto actualizado.
- Se sube por el medio indicado por el docente (aula virtual / plataforma del curso).

---

## Procedimiento

En la Semana 4 se incorporaron relaciones entre Models (`OneToOneField`, `ForeignKey` y `ManyToManyField` con `through`) sobre la aplicación ya persistente desde la Semana 3. En esta sesión **no se agregan Models ni relaciones nuevas**: se incorpora el **Django Admin**, la interfaz de administración que Django genera automáticamente a partir de los Models ya registrados, permitiendo gestionar esos datos relacionados sin escribir una View propia.

El laboratorio tiene **dos partes**:

1. **Parte 1:** retomar la app de la Semana 4 y registrar sus modelos (incluidas las tres relaciones) en el Django Admin, personalizándolo con `ModelAdmin` e Inlines.
2. **Parte 2:** hacer lo mismo sobre la investigación propia (las siete entidades ampliadas en la Parte 2 del laboratorio de la Semana 4), cumpliendo el checklist obligatorio.

**Idea central:** el Django Admin no reemplaza al Model ni al ORM: los **reutiliza**. El mismo Model y las mismas relaciones ya implementadas son las que el Admin expone automáticamente; el estudiante decide cómo presentarlas (`list_display`, `search_fields`, `list_filter`) y cómo editar relaciones desde una sola pantalla (Inlines).

### Flujo integral que se debe comprender

```
Staff autenticado → URL /admin/... → Django Admin autentica y enruta
    → ModelAdmin → Manager / QuerySet → Django ORM → SQLite
    → Template (generado automáticamente por el Admin) → Response
```

Al finalizar, el estudiante debe ser capaz de registrar modelos relacionados en el Django Admin, personalizar `ModelAdmin` con `list_display`, `search_fields` y `list_filter`, y exponer relaciones 1:1 y N:M mediante `StackedInline` y `TabularInline`, reconociendo qué resuelve el Admin y qué seguirá requiriendo una View y un Template propios.

---

## Enunciados

### PARTE 1 — Administrar en el Django Admin la aplicación de la Semana 4

| # | Ejercicio | Qué hacer |
|---|---|---|
| 1 | Recuperar la aplicación de la Semana 4 | Abrir la app de la Semana 4, identificar entidad principal, las 3 relaciones implementadas y el estado de migraciones |
| 2 | Crear el superusuario | `python manage.py createsuperuser`, iniciar sesión en `/admin/`, captura del panel inicial |
| 3 | Registrar los modelos en el Admin | En `admin.py`, registrar todos los modelos de la Semana 4 con `admin.site.register()`; verificar que aparecen |
| 4 | Personalizar con `ModelAdmin` | Reemplazar ≥2 registros simples por una clase `ModelAdmin`: `list_display` con los campos más relevantes y `search_fields` en al menos uno |
| 5 | Agregar `list_filter` | Configurar `list_filter` en ≥1 modelo con un campo que tenga sentido filtrar (fecha, categoría, estado); captura del panel de filtros |
| 6 | Exponer la relación 1:1 con `StackedInline` | `StackedInline` para la entidad de la relación `OneToOneField`, editable desde la pantalla de la entidad principal |
| 7 | Exponer la relación N:M con `TabularInline` | `TabularInline` para el modelo intermedio (`through`) del `ManyToManyField`, mostrando sus atributos propios como columnas editables |
| 8 | Verificar el flujo completo en el Admin | Crear, editar y eliminar ≥1 registro de cada tipo de relación desde el panel; explicar qué resuelve el Admin y qué seguiría necesitando una View y un Template propios |

### PARTE 2 — Administrar la investigación propia (ampliada en la Semana 4)

Trabaja sobre la base de datos ampliada de la investigación propia: las cinco entidades originales + la entidad 1:1 + el modelo intermedio N:M.

**Ejercicio 9 — Registrar las siete entidades en el Admin**
Registrar en `admin.py` las siete entidades mediante `admin.site.register()`. Verificar que todas aparecen en el panel.

**Checklist obligatorio antes de continuar — Parte 2**

| # | Criterio | Verificación |
|---|---|---|
| 1 | Las 7 entidades (5 originales + 1:1 + modelo intermedio N:M) están registradas en el Admin | Conteo directo en `admin.py` |
| 2 | ≥3 modelos usan una clase `ModelAdmin` (no solo `register()` sin personalizar) | Código + captura del listado |
| 3 | ≥2 modelos tienen `list_display` mostrando campos relevantes, no solo `__str__` | Captura del listado |
| 4 | ≥1 modelo tiene `search_fields` configurado y funcionando | Captura de una búsqueda |
| 5 | ≥1 modelo tiene `list_filter` configurado y funcionando | Captura del panel de filtros |
| 6 | La relación `OneToOneField` se expone con `StackedInline` en la entidad principal | Captura del formulario con el Inline |
| 7 | El modelo intermedio N:M se expone con `TabularInline`, mostrando sus atributos propios | Captura del formulario con el Inline |
| 8 | ≥1 operación completa de creación, edición y eliminación desde el Admin (no solo lectura) | Capturas antes/después |
| 9 | Explicación escrita de qué resuelve el Admin para esta investigación y qué seguiría necesitando View/Template propios | Párrafo de justificación |

| # | Ejercicio | Qué hacer |
|---|---|---|
| 10 | Personalizar `ModelAdmin` | `ModelAdmin` en ≥3 de las 7 entidades, `list_display` relevante; `search_fields` en ≥1, `list_filter` en ≥1 otra, con campos que tengan sentido para la problemática |
| 11 | `StackedInline` para la relación 1:1 | Editable en la misma pantalla de la entidad principal |
| 12 | `TabularInline` para el modelo intermedio N:M | Columnas editables con los atributos propios (cantidad, fecha, estado...) |
| 13 | Verificar el flujo completo | Crear, editar, eliminar ≥1 registro relacionado (usando Inlines); capturas antes/después; comprobar persistencia en SQLite |
| 14 | Publicar en GitHub | Actualizar `requirements.txt` y `README.md` describiendo qué se registró/personalizó en el Admin; commit y push; incluir URL del repo en el documento |

---

## Entregables

- Cada enunciado con su respuesta, justificación y captura de pantalla (especialmente código de `admin.py` y el panel del Django Admin en el navegador).
- Repositorio en GitHub actualizado: `requirements.txt`, `README.md` y el código correspondiente a cada integrante.
- Dirección (URL) del repositorio de GitHub incluida explícitamente en el documento, conforme al Modo de entrega.

---

## Aplicación al proyecto real (`empresariales/django_project/`)

Las tres relaciones ya existen en ambas apps (ver [TEMA_04_Relaciones_Models.md](apuntes_previos/TEMA_04_Relaciones_Models.md)):

| App | Entidad principal | 1:1 (`StackedInline`) | 1:N (`ForeignKey`) | N:M `through` (`TabularInline`) |
|---|---|---|---|---|
| `biblioteca` | `Socio` / `Libro` | `CarnetSocio` ↔ `Socio` | `Categoria` → `Libro` | `Prestamo` (`Socio` ↔ `Libro`) |
| `vet` | `Cita` | `FichaClinica` ↔ `Cita` | `Veterinario` → `Cita` | `ConsumoInsumo` (`Cita` ↔ `Insumo`) |

**Plan de trabajo sugerido para la Parte 1:**

1. `createsuperuser` en `django_project/src/` (Ejercicio 2).
2. `admin.py` de la app elegida: `register()` de todas las entidades (Ejercicio 3).
3. `ModelAdmin` con `list_display` en ≥2 modelos + `search_fields` en 1 (Ejercicio 4).
   - Ej. `biblioteca`: `Libro` (`list_display = ('titulo', 'autor', 'categoria', 'anio_publicacion')`, `search_fields = ('titulo', 'autor', 'isbn')`).
4. `list_filter` — ej. `Prestamo` por `estado`, o `Libro` por `categoria` (Ejercicio 5).
5. `StackedInline` de `CarnetSocio` dentro de `SocioAdmin`, o `FichaClinica` dentro de `CitaAdmin` (Ejercicio 6).
6. `TabularInline` de `Prestamo` dentro de `SocioAdmin`/`LibroAdmin`, o `ConsumoInsumo` dentro de `CitaAdmin` (Ejercicio 7).
7. CRUD completo desde el panel + justificación escrita Admin vs. View/Template propio (Ejercicio 8).

Pendiente por definir contigo: **con qué app empezamos** (`biblioteca`, `vet`, o ambas) y si ya tienes armadas las 7 entidades de tu investigación propia para la Parte 2.
