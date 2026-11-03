# GLAB-S03 — Guía de Laboratorio 03 (Semana 3)

**Curso:** Desarrollo de Aplicaciones Empresariales
**Carrera:** Desarrollo de Software
**Estudiante:** Bestard Aroche, Yunior
**Sección:** 4 - C24 - Sección CD
**Tema:** Django Models, migraciones, Django ORM y SQLite — flujo CRUD completo

> Fuente: `GLAB-S03-YBESTARD-2026-02.docx` (extracción de la información relevante para el desarrollo).

---

## Capacidades

- Diseñar e implementar **Models** en Django, definiendo entidades, campos y relaciones básicas de acuerdo con los requisitos de una problemática planteada.
- Aplicar **Django ORM** y **SQLite** para gestionar datos persistentes, utilizando migraciones y operaciones de creación, consulta, actualización y eliminación de registros.
- Implementar y explicar el **flujo CRUD completo** en Django, integrando URLs, Views, Models, Templates y operaciones ORM para resolver una problemática real.

## Seguridad

- Está prohibida la manipulación del hardware, conexiones eléctricas o de red, así como la ingesta de alimentos y bebidas.
- Ubicar maletines y/o mochilas en el lugar destinado para tal fin.
- Dejar la mesa de trabajo y la silla utilizada limpias y ordenadas.

## Fundamento teórico

- Revisar el material de la semana correspondiente antes del desarrollo del laboratorio.

## Normas empleadas

- No aplica.

## Recursos

- Cada estudiante trabaja con una computadora con **Windows 11**.
- Los softwares requeridos ya están instalados en los laboratorios.
- Se requiere **Python 3.10 o superior**, **Django 5**, un editor de código (**Visual Studio Code**) y una **cuenta de GitHub** para el control de versiones.

## Metodología

- El desarrollo del laboratorio es **individual**.

---

## Procedimiento

En la Semana 2 se trabajó la estructura básica de una aplicación Django con el patrón **MVT** (formularios, Views, URLs y Templates), pero los datos se almacenaban de forma temporal **en memoria**. En este laboratorio se convierten esas estructuras en **información persistente** mediante Django Models, migraciones, Django ORM y SQLite, de modo que los registros se mantengan aunque se reinicie el servidor.

El laboratorio tiene **dos partes**:

1. **Parte 1:** retomar la app de la Semana 2 y reemplazar los datos estáticos por Models reales y operaciones ORM (consulta y registro persistentes).
2. **Parte 2:** investigar una problemática real, identificar sus requisitos y diseñar una solución con varias entidades, relaciones entre Models y operaciones CRUD completas.

### Flujo integral que se debe comprender

```
Request → URL → View → Model → Manager / QuerySet → Django ORM → SQLite → Template → Response
```

Al finalizar, el estudiante debe ser capaz de: diseñar Models, generar y aplicar migraciones, usar SQLite como mecanismo de persistencia e implementar operaciones CRUD **sin escribir SQL manual**. También debe distinguir entre **modificar datos (CRUD)** y **modificar la estructura de la BD (migraciones)**.

---

## PARTE 1 — Migración del trabajo de la Semana 2 a Django ORM y SQLite

### Ejercicio 1 — Recuperar y analizar la aplicación anterior
Abrir la app de la Semana 2 e identificar: la **entidad principal**, los datos almacenados en memoria, las **Views, URLs, formularios y Templates**. Explicar brevemente qué ocurre con los registros agregados cuando se **reinicia el servidor**.

### Ejercicio 2 — Convertir la entidad en un Django Model
Reemplazar la estructura de datos estática de `models.py` por un **Django Model real**. Mantener los campos definidos en el laboratorio anterior y usar tipos de datos apropiados de Django.

### Ejercicio 3 — Crear la estructura persistente de datos
Generar y aplicar las **migraciones** para crear la tabla en SQLite. Documentar con capturas el resultado de `makemigrations`, `migrate` y `showmigrations`.

### Ejercicio 4 — Implementar la consulta mediante ORM
Modificar la View del listado para que **deje de leer una lista Python** y obtenga los datos mediante **Django ORM** (QuerySet). Verificar que los registros de SQLite se muestran correctamente en el Template.

### Ejercicio 5 — Implementar el registro mediante ORM
Adaptar la funcionalidad de creación de la Semana 2 para que los datos del formulario se **almacenen de forma persistente** con Django ORM. Tras el registro, **redirigir al listado** y comprobar que el dato permanece tras reiniciar el servidor.

### Ejercicio 6 — Analizar el flujo de persistencia
Documentar el recorrido completo de una operación de **consulta** y una de **creación**:

```
Request → URL → View → Model → Manager / QuerySet → Django ORM → SQLite → View → Context → Template → Response
```

Identificar además qué **operación SQL** representa conceptualmente cada acción realizada mediante ORM.

---

## PARTE 2 — Investigación y desarrollo de una nueva solución persistente

### Ejercicio 7 — Investigar una problemática real
Investigar una problemática real resoluble con una **aplicación empresarial web**. Debe manejar varios tipos de información y justificar la existencia de **múltiples entidades**. Describir el problema, los usuarios involucrados y el proceso a mejorar.

### Ejercicio 8 — Definir los requisitos funcionales
Redactar entre **8 y 12 requisitos funcionales** derivados de la problemática. Deben contemplar como mínimo operaciones de **crear, listar, actualizar y eliminar** información.

### Ejercicio 9 — Diseñar el modelo de datos
Diseñar como mínimo **cinco entidades**:

- **Tres** entidades independientes (no relacionadas entre sí).
- **Dos** entidades relacionadas mediante **ForeignKey**.

Para cada entidad definir: nombre, campos, tipos de datos, obligatoriedad, clave primaria y clave foránea cuando corresponda. **Justificar** por qué cada entidad y cada relación son necesarias.

### Ejercicio 10 — Representar las relaciones
Elaborar un **diagrama sencillo** del modelo de datos con las cinco entidades y la relación entre las dos entidades vinculadas.

Ejemplo conceptual:

```
Entidad A     Entidad B     Entidad C

Entidad D
   1
   │
   │
   N
Entidad E
```

La problemática, los nombres de las entidades y los campos los define el estudiante a partir de su investigación.

### Ejercicio 11 — Crear la aplicación Django
Crear una **nueva App Django** para la problemática. Registrarla en `INSTALLED_APPS` y configurar sus **URLs** dentro del Project.

### Ejercicio 12 — Implementar los Models
Traducir el diseño del Ejercicio 9 a **Django Models**. Implementar las cinco entidades y configurar la relación **ForeignKey** entre las dos entidades relacionadas.

### Ejercicio 13 — Crear la base de datos mediante migraciones

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

### Ejercicio 14 — Implementar CREATE
Funcionalidad web para registrar nuevos datos mediante Django ORM. Tras guardar, **redirigir al listado**.

```
Formulario → POST → View → ORM → INSERT → SQLite → redirect → listado
```

### Ejercicio 15 — Implementar READ
Pantalla de **listado** para cada entidad usando QuerySets. Datos obtenidos desde SQLite vía ORM y mostrados con Templates.

```python
Model.objects.all()
Model.objects.filter(...)
Model.objects.order_by(...)
```

### Ejercicio 16 — Implementar UPDATE
Cada registro debe poder actualizarse. La View recupera el objeto, modifica sus propiedades y guarda con Django ORM.

```
Seleccionar registro → GET → formulario con datos actuales → POST → modificar objeto → save() → ORM → UPDATE → SQLite → redirect → listado actualizado
```

### Ejercicio 17 — Implementar DELETE
Cada registro debe poder eliminarse. Mostrar primero una **confirmación** y eliminar mediante petición **POST**.

```
Seleccionar registro → confirmación → POST → delete() → ORM → DELETE → SQLite → redirect → listado actualizado
```

### Ejercicio 18 — Verificar las entidades relacionadas
Pruebas que demuestren que la relación entre las dos entidades funciona: registrar datos asociados, consultar registros relacionados y comprobar la **clave foránea** generada por Django.

### Ejercicio 19 — Verificar el CRUD completo
Para cada entidad, comprobar:

| Operación | SQL |
|-----------|-----|
| CREATE | INSERT |
| READ   | SELECT |
| UPDATE | UPDATE |
| DELETE | DELETE |

Todo mediante Django ORM y SQLite, **sin SQL manual**.

### Ejercicio 20 — Documentar el flujo completo
Elegir al menos una entidad y documentar con capturas el recorrido de las **cuatro operaciones CRUD**:

```
Navegador → URL → View → Model → Django ORM → SQLite → redirect / render → Template → Navegador
```

### Ejercicio 21 — Publicar en GitHub
*(rotulado como "Ejercicio 10" en el documento original)*
Actualizar `requirements.txt` y `README.md` describiendo la problemática, los requisitos y la App creada. Hacer **commit y push** al repositorio del equipo.

---

## Entregables

- **Documento de requisitos:** problemática elegida y lista de requisitos funcionales.
- **Diseño del modelo de datos:** entidad principal, campos, tipos y justificación.
- **Código fuente completo de la nueva App:** `models.py`, `views.py`, `urls.py`, `forms.py` y templates (listado y formulario).
- **Capturas de pantalla del flujo funcionando:** listado de registros, formulario de creación y el nuevo registro reflejado en el listado.
- **Repositorio en GitHub actualizado**, con `requirements.txt`, `README.md` y el código correspondiente a cada integrante del equipo, según el formato de evidencia indicado (nombre, título, captura, código, explicación y casos de prueba).

## Conclusiones

*(A completar por el estudiante.)*
