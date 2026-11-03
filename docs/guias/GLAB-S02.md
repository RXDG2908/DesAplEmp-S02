# Laboratorio 02 — Nueva App con datos estáticos y formulario

Instrucciones para el laboratorio de la Semana 2 del curso
**Desarrollo de Aplicaciones Empresariales** (4 - C24 - Sección CD).
Fuente: `GLAB-S02-YBESTARD-2026-02.docx`. Estudiante: **Renzo León**.

## Capacidades

1. Identificar y formalizar los requisitos de una problemática real (tienda,
   biblioteca, reservas, etc.) como base para el diseño de una aplicación Django.
2. Diseñar e implementar una nueva App Django (Model, View, URL, Template)
   conectada a un proyecto existente, aplicando el patrón MVT.
3. Implementar formularios (Forms) que traduzcan los requisitos identificados en
   una funcionalidad real de captura y persistencia de datos.

## Fundamento teórico

Revisar el material de la semana correspondiente antes del desarrollo del
laboratorio — ver [CLAUDE.md](CLAUDE.md) (Sesión 02: Project, App, MVT,
Request/Response).

## Introducción al laboratorio

En las sesiones anteriores se construyó y extendió el proyecto `DjangoInicial`,
comprendiendo cómo Django organiza una aplicación mediante el patrón MVT:
Project, Apps, Models, Views, URLs y Templates. En este laboratorio se da un
paso más cercano a cómo se trabaja en un proyecto real: en lugar de partir de un
modelo ya definido, se investiga una problemática real, se capturan sus
requisitos, y se traducen esos requisitos en una aplicación Django funcional,
construida como una nueva App conectada al proyecto ya conocido (`config`/`core`).

Para mantener el foco en el flujo MVT y en cómo un formulario transforma datos
en un response, esta aplicación **no usa base de datos**: los datos se definen
de forma estática dentro de `models.py` (por ejemplo, como una lista de
diccionarios), y las vistas leen y agregan información directamente sobre esa
estructura en memoria, sin migraciones ni panel de administración.

Problemática libre: tienda de barrio, biblioteca, veterinaria, alquiler de
equipos, reserva de citas, control de asistencia, u otra que resulte relevante.

## Recursos

- Computadora con Windows 11 (softwares ya instalados en los laboratorios).
- Python 3.10 o superior, Django 5, Visual Studio Code, cuenta de GitHub.

## Metodología

El desarrollo del laboratorio es **individual**.

## Los 10 ejercicios

1. **Investigar una problemática real.** Elegir una problemática cotidiana
   resoluble con una app web y redactar en 3-5 líneas en qué consiste y quién la
   usaría.
2. **Capturar los requisitos.** Listar 4-6 requisitos funcionales, cada uno como
   una acción concreta que el sistema debe permitir (ej. *"el sistema debe
   permitir registrar un producto"*).
3. **Diseñar el modelo de datos.** A partir de los requisitos, identificar la
   entidad principal (Producto, Libro, Cita, Equipo...) y definir sus campos
   (nombre, tipo de dato, obligatorio o no) con una justificación breve de cada
   uno.
4. **Crear la nueva App.** Dentro del proyecto base (`config`/`core`), crear una
   App con nombre representativo (`store`, `library`, `bookings`...) y
   registrarla en `INSTALLED_APPS`.
5. **Implementar el Model con datos estáticos.** Traducir el diseño del
   Ejercicio 3 en `models.py` como una lista de diccionarios (o de objetos de
   una clase simple) con **al menos 5 registros** de ejemplo. No se usan
   migraciones ni base de datos: esta lista es la única fuente de datos.
6. **Implementar el listado (View + URL + Template).** Vista que recorre la
   lista de `models.py` y la muestra en un template que hereda de `base.html`,
   siguiendo el mismo patrón que `core`.
7. **Implementar el formulario (Forms).** `forms.py` con un `forms.Form` (no
   `ModelForm`, porque no hay modelo de base de datos) cuyos campos
   correspondan a los requisitos del Ejercicio 2.
8. **Implementar la vista de creación.** Vista que muestra el formulario del
   Ejercicio 7, procesa el envío (`POST`), valida los datos y agrega el nuevo
   registro a la lista en memoria de `models.py`; luego redirige al listado para
   confirmar que el nuevo dato aparece. Los datos agregados **se pierden al
   reiniciar el servidor** — esto es esperado y debe mencionarse en la
   documentación.
9. **Verificación del flujo completo.** Navegar la app de principio a fin
   (listado → crear → volver al listado con el nuevo dato reflejado) y
   documentar con capturas el recorrido `Request → URL → View → Model (datos
   estáticos) → Template → Response`. Explicar cómo la nueva App convive con
   `core` dentro del mismo Project.
10. **Publicar en GitHub.** Actualizar `requirements.txt` y `README.md`
    describiendo la problemática, los requisitos y la App creada. Commit y push
    al repositorio del equipo.

## Entregables

- Documento de requisitos: problemática elegida (Ej. 1) y lista de requisitos
  funcionales (Ej. 2).
- Diseño del modelo de datos: entidad principal, campos, tipos y justificación
  (Ej. 3).
- Código fuente completo de la nueva App: `models.py` (con los datos
  estáticos), `views.py`, `urls.py`, `forms.py` y templates (listado y
  formulario).
- Capturas de pantalla del flujo funcionando: listado de registros, formulario
  de creación, y el nuevo registro reflejado en el listado.
- Explicación del flujo MVT aplicado a su caso (Ej. 9), incluyendo cómo la App
  se conecta con `core` dentro del mismo Project.
- Repositorio en GitHub actualizado, con `requirements.txt`, `README.md` y el
  código correspondiente a cada integrante del equipo, según el formato de
  evidencia indicado en las instrucciones del laboratorio (nombre, título,
  captura, código, explicación y casos de prueba).
- Conclusiones.

## Seguridad del laboratorio

Prohibido manipular hardware, conexiones eléctricas o de red, e ingerir
alimentos y bebidas. Maletines y mochilas en el lugar destinado. Dejar mesa y
silla limpias.
