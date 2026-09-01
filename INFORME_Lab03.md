# Informe — Laboratorio 03: Models, Django ORM y SQLite

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Lucas Inga - Renzo Leon

## Ejercicio 1 — Recuperar y analizar la aplicación anterior

**Entidad principal:** `Cita`, con los campos `mascota`, `dueno`, `servicio`,
`fecha`, `hora` y `estado`.

**Datos en memoria:** en la Semana 2, `Cita` era una clase Python común (no
heredaba de `models.Model`); la única fuente de datos era la lista `citas`
definida en `models.py`.

**Views/URLs/Forms/Templates:** `cita_list` (listado), `cita_crear`
(formulario `CitaForm` que hacía `citas.append(...)`), rutas
`vet:cita_list`/`vet:cita_crear`, templates `cita_list.html`/`cita_form.html`.

**Qué pasa al reiniciar el servidor:** la lista vive solo en la memoria del
proceso; al reiniciar el servidor, vuelve a sus 5 valores iniciales y
cualquier cita agregada durante la ejecución se pierde por completo.