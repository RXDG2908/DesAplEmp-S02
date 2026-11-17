# Índice maestro de semanas — Desarrollo de Aplicaciones Empresariales

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Repositorio:** https://github.com/RXDG2908/DesAplEmp-S02
**Proyecto:** [`django_project/`](django_project/README.md) — un solo Project
Django (`config`) con dos Apps: `vet` (reserva de citas de una veterinaria,
Parte 1, Renzo) y `biblioteca` (biblioteca comunitaria, Parte 2, Lucas).

Cada semana suma una capa sobre la misma aplicación: primero sin base de
datos, después con ORM, relaciones, Admin, plantillas y ORM avanzado.

---

## Resumen

| Semana | Tema | Qué se hizo en `vet` | Exposición |
|---|---|---|---|
| 1 | Fundamentos de Django | Proyecto de ejemplo DjangoInicial (`config` / `core` / `Item`) | — |
| 2 | Arquitectura MVT, Request/Response | App `vet` sin base de datos: lista en memoria, listado y formulario | [EXPOSICION_Lab02.md](EXPOSICION_Lab02.md) |
| 3 | Models, Django ORM y SQLite | `Cita` pasa a ser un Model; migraciones; CRUD con el ORM | [EXPOSICION_Lab03_Parte1.md](EXPOSICION_Lab03_Parte1.md) |
| 4 | Relaciones entre Models | 1:1 `FichaClinica`, 1:N `Veterinario`, N:M `Insumo` vía `ConsumoInsumo` | [EXPOSICION_Lab04_Parte1.md](EXPOSICION_Lab04_Parte1.md) |
| 5 | Django Admin | `ModelAdmin`, `list_display`, filtros e Inlines para las relaciones | [EXPOSICION_Lab05_Parte1.md](EXPOSICION_Lab05_Parte1.md) |
| 6 | Motor de plantillas | Herencia, filtros, comentarios, `include` y escape automático | [EXPOSICION_Lab06_Parte1.md](EXPOSICION_Lab06_Parte1.md) |
| 7 | ORM avanzado | `transaction.atomic` + `F()`, `aggregate`/`annotate`, QuerySet propio, N+1 | [EXPOSICION_Lab07_Parte1.md](EXPOSICION_Lab07_Parte1.md) |

---

## Semana 1 — Fundamentos de Django

> **Palabras clave:** **Project**, **App**, **venv**, `startproject`, `startapp`, `runserver`

- **Tema:** qué es Django, Project vs. App, entorno virtual, primer proyecto
  y primer `admin.site.register()`.
- **Laboratorio:** proyecto de ejemplo DjangoInicial (`config` / `core` /
  modelo `Item`). No está en este repositorio.
- **Material:** [apuntes_previos/TEMA_01_Fundamentos_Django.md](apuntes_previos/TEMA_01_Fundamentos_Django.md)

## Semana 2 — Arquitectura de Django: MVT y Request/Response

> **Palabras clave:** **MVT**, **Request/Response**, **URL → View → Template**, **Context**, **herencia** (`extends`/`block`), **`forms.Form`**, **Post/Redirect/Get**

- **Tema:** Project vs. App, patrón MVT (y su diferencia con MVC), URLs,
  Views, Templates, Context, `forms.Form`.
- **Laboratorio 02:** crear la App `vet` con datos estáticos (lista en
  memoria), listado ordenado, formulario con validación de horario y vista
  de creación con Post/Redirect/Get. Sin migraciones ni Admin.
- **Archivos:** teoría en [CLAUDE.md](CLAUDE.md) y
  [PPT-S02-YBESTARD-2026-02.pptx](PPT-S02-YBESTARD-2026-02.pptx) · guía
  [GLAB-S02.md](GLAB-S02.md) · informe [INFORME_Lab02.md](INFORME_Lab02.md) ·
  Word [GLAB-S02-YBESTARD-2026-02.docx](GLAB-S02-YBESTARD-2026-02.docx) ·
  capturas en `Capturas/` (`4.png` … `10.png`)
- **Apuntes:** [apuntes_previos/TEMA_02_MVT_URLs_Views_Templates.md](apuntes_previos/TEMA_02_MVT_URLs_Views_Templates.md)
- **Exposición:** [EXPOSICION_Lab02.md](EXPOSICION_Lab02.md)

## Semana 3 — Models, Django ORM y SQLite

> **Palabras clave:** **Model**, **ORM**, **Manager/QuerySet**, **migraciones** (`makemigrations`/`migrate`), **CRUD**, **SQLite**, **persistencia**

- **Tema:** Django Model, Manager y QuerySet, `makemigrations` / `migrate`,
  CRUD con el ORM, Post/Redirect/Get.
- **Laboratorio 03:** Parte 1 (`vet`, Ej. 1-6): la lista en memoria se
  reemplaza por el Model `Cita`, migración `0001_initial`, consulta con
  `order_by` y registro con `create`. Parte 2 (`biblioteca`, Lucas): App
  nueva con 5 entidades y CRUD completo.
- **Archivos:** guía [GLAB-S03.md](GLAB-S03.md) · informe
  [INFORME_Lab03.md](INFORME_Lab03.md) · Word
  [GLAB-S03-YBESTARD-2026-02.docx](GLAB-S03-YBESTARD-2026-02.docx) ·
  capturas en `Capturas/Semana03/`
- **Apuntes:** [apuntes_previos/TEMA_03_ORM_Migraciones_CRUD.md](apuntes_previos/TEMA_03_ORM_Migraciones_CRUD.md)
- **Exposición:** [EXPOSICION_Lab03_Parte1.md](EXPOSICION_Lab03_Parte1.md)

## Semana 4 — Relaciones entre Models

> **Palabras clave:** **1:1** (`OneToOneField`), **1:N** (`ForeignKey`), **N:M** (`ManyToManyField` + `through`), **`on_delete`**, **`related_name`**, **N+1**

- **Tema:** `OneToOneField`, `ForeignKey`, `ManyToManyField` con `through`,
  `on_delete`, `related_name`, `select_related` / `prefetch_related`.
- **Laboratorio 04:** Parte 1 (`vet`): `FichaClinica` (1:1), `Veterinario`
  (1:N), `Insumo` + `ConsumoInsumo` (N:M), migración `0002`, vista
  `cita_detalle` y template con acceso directo, inverso e intermedio. Parte 2
  (`biblioteca`, Lucas): `CarnetSocio` (1:1) y `Prestamo` (N:M).
- **Archivos:** no hay informe ni guía en el repositorio; el resumen está en
  [django_project/README.md](django_project/README.md) · datos de prueba en
  `django_project/src/cargar_datos.py`
- **Apuntes:** [apuntes_previos/TEMA_04_Relaciones_Models.md](apuntes_previos/TEMA_04_Relaciones_Models.md)
- **Exposición:** [EXPOSICION_Lab04_Parte1.md](EXPOSICION_Lab04_Parte1.md)

## Semana 5 — Django Admin

> **Palabras clave:** **Admin**, **superusuario**, **`ModelAdmin`**, **`list_display`/`search_fields`/`list_filter`**, **Inlines** (`StackedInline`/`TabularInline`)

- **Tema:** superusuario, `admin.site.register`, `ModelAdmin`
  (`list_display`, `search_fields`, `list_filter`), `StackedInline` y
  `TabularInline`.
- **Laboratorio 05:** Parte 1 (`vet`, Ej. 1-8): registrar `Cita`,
  `Veterinario` e `Insumo`; la ficha y los consumos como Inlines dentro de
  la Cita. Parte 2 (`biblioteca`, Lucas): `SocioAdmin`, `LibroAdmin`,
  `PrestamoAdmin` con Inlines.
- **Archivos:** guía [GLAB-S05.md](GLAB-S05.md) · informe
  [INFORME_Lab05.md](INFORME_Lab05.md) · pendientes de Lucas en
  [LUCAS_TODO_Lab05.md](LUCAS_TODO_Lab05.md)
- **Exposición:** [EXPOSICION_Lab05_Parte1.md](EXPOSICION_Lab05_Parte1.md)
  (y su guion en voz alta, [GUION-Lab05-Parte1.md](GUION-Lab05-Parte1.md))

## Semana 6 — Motor de plantillas de Django

> **Palabras clave:** **herencia de plantillas**, **bloques**, **filtros**, **comentarios `{# #}`**, **`include`**, **escape automático (XSS)**

- **Tema:** herencia (`extends` / `block`), filtros, comentarios `{# #}`,
  `include` y escape automático; plantillas propias vs. Admin.
- **Laboratorio 06:** Parte 1 (`vet`, Ej. 1-8): filtros `floatformat:2` y
  `title`, fragmento `_veterinario_info.html`, prueba con `<script>`.
  Parte 2 (`biblioteca`, Lucas): fragmento `_prestamo_campos.html`.
- **Archivos:** informe [INFORME_Lab06.md](INFORME_Lab06.md) · Word
  [GLAB-S06-YBESTARD-2026-02-RESUELTO.docx](GLAB-S06-YBESTARD-2026-02-RESUELTO.docx) ·
  capturas en `Capturas/Lab06/`
- **Exposición:** [EXPOSICION_Lab06_Parte1.md](EXPOSICION_Lab06_Parte1.md)

## Semana 7 — ORM avanzado

> **Palabras clave:** **`transaction.atomic`**, **`F()`**, **`aggregate`** vs. **`annotate`**, **QuerySet personalizado**, **N+1** (`select_related`/`prefetch_related`)

- **Tema:** `transaction.atomic`, expresiones `F()`, `aggregate` vs.
  `annotate`, QuerySet personalizado con `as_manager()`, problema N+1.
- **Laboratorio 07:** Parte 1 (`vet`, Ej. 1-8): pantalla "Registrar consumo"
  con transacción, página `/reporte/`, `CitaQuerySet` (`con_estado`,
  `proximas`), medición 6 → 1 y 15 → 3 consultas. Parte 2 (`biblioteca`,
  Lucas): `PrestamoQuerySet` y lo equivalente.
- **Archivos:** informe [INFORME_Lab07.md](INFORME_Lab07.md) · Word
  [GLAB-S07-YBESTARD-2026-02-RESUELTO.docx](GLAB-S07-YBESTARD-2026-02-RESUELTO.docx) ·
  capturas en `Capturas/Lab07/` · scripts `cargar_lab07.py` y `medir_n1.py`
  en `django_project/src/`
- **Exposición:** [EXPOSICION_Lab07_Parte1.md](EXPOSICION_Lab07_Parte1.md)

---

## Otros índices del repositorio

- [INDICE_VET.md](INDICE_VET.md) — súper índice de la App `vet` y preguntas
  del profesor.
- [INDICE_FUNCIONES.md](INDICE_FUNCIONES.md) — índice de funciones y sondeo
  del código (S02/S03).
- [apuntes_previos/INDICE.md](apuntes_previos/INDICE.md) — apuntes de las
  Semanas 1 a 4.
