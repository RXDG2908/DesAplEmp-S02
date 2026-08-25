# Informe — Laboratorio 02: Nueva App con datos estáticos y formulario

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiante:** Renzo León
**Problemática elegida:** Reserva de citas — Veterinaria

> Ver enunciado completo en [GLAB-S02.md](GLAB-S02.md). Este informe se va
> completando ejercicio por ejercicio conforme avanza el laboratorio.

---

## Ejercicio 1 — Problemática

Una veterinaria de barrio recibe las solicitudes de cita por llamada telefónica
o mensaje directo, sin ningún registro centralizado. Esto provoca que se
encimen citas en el mismo horario, que se olviden solicitudes y que no haya
forma rápida de saber qué horarios del día ya están ocupados. Se necesita una
aplicación web sencilla donde la recepción pueda registrar cada cita (mascota,
dueño, servicio, fecha y hora) y consultar el listado del día para organizar la
agenda. La usarían principalmente el/la recepcionista y el veterinario a cargo
de atender.

---

## Ejercicio 2 — Requisitos funcionales

> Laboratorio en **grupo de 2**: el profesor pide **6 requisitos funcionales
> por integrante** (12 en total para el sistema completo). Los siguientes son
> los 6 requisitos a cargo de **Renzo León**; el otro integrante documenta sus
> propios 6 en su parte del informe.

1. El sistema debe permitir **registrar una nueva cita**, indicando la mascota,
   el dueño, el servicio solicitado, la fecha y la hora.
2. El sistema debe permitir **ver el listado de citas registradas**.
3. El sistema debe permitir **identificar el servicio solicitado** para cada
   cita (consulta, vacunación, cirugía, baño, u otro).
4. El sistema debe permitir **distinguir el estado de la cita** (pendiente,
   confirmada, atendida) para dar seguimiento.
5. El sistema debe permitir **ordenar/consultar las citas por fecha y hora**,
   para evitar que dos citas queden en el mismo horario.
6. El sistema debe permitir **identificar al dueño responsable de cada
   mascota**, para poder contactarlo ante cualquier cambio o confirmación de
   la cita.

### Requisitos del segundo integrante _(reemplazar nombre)_

7. El sistema debe permitir **cancelar una cita registrada**.
8. El sistema debe permitir **ver el detalle completo de una cita** al
   seleccionarla desde el listado.
9. El sistema debe permitir **asignar un veterinario responsable** a cada
   cita.
10. El sistema debe permitir **filtrar las citas por estado** (pendiente,
    confirmada, atendida).
11. El sistema debe permitir **buscar citas por nombre de mascota o de
    dueño**.
12. El sistema debe permitir **ver cuántas citas hay registradas por día**,
    para conocer la carga de la agenda.

---

## Ejercicio 3 — Diseño del modelo de datos

**Entidad principal:** `Cita`

| Campo | Tipo de dato | ¿Obligatorio? | Justificación |
|---|---|---|---|
| `mascota` | Texto corto (`CharField`) | Sí | Identifica al paciente de la cita (Requisito 1). |
| `dueno` | Texto corto (`CharField`) | Sí | Permite identificar y contactar al propietario responsable (Requisitos 1 y 6). |
| `servicio` | Texto corto con opciones (`CharField` + `choices`: consulta, vacunación, cirugía, baño) | Sí | Define qué atención se brindará (Requisito 3). |
| `fecha` | Fecha (`DateField`) | Sí | Ubica la cita en el calendario y permite ordenar/filtrar por día (Requisito 5). |
| `hora` | Hora (`TimeField`) | Sí | Evita que dos citas se crucen en el mismo horario (Requisito 5). |
| `estado` | Texto corto con opciones (`CharField` + `choices`: pendiente, confirmada, atendida; por defecto `pendiente`) | No (tiene valor por defecto) | Permite dar seguimiento a la cita a lo largo del día (Requisito 4). |

Como no hay base de datos, estos campos se representarán como claves de un
diccionario dentro de una lista en `models.py` (Ejercicio 5), y el formulario
de creación (Ejercicio 7) tendrá un campo por cada uno de `mascota`, `dueno`,
`servicio`, `fecha` y `hora` (el `estado` se asigna automáticamente como
`pendiente` al crear la cita).

---

## Ejercicio 4 — Crear la nueva App

**Captura:** la carpeta `Semana 2/django_project/src/vet/` generada y el
bloque `INSTALLED_APPS` de `settings.py` con `'vet'` añadido.

**Explicación:** A diferencia del Laboratorio 01, esta App vive en su **propio**
proyecto Django dentro de `Semana 2/django_project/`, con su propio entorno
virtual y su propio `Project` (`config`), guiándose por la estructura de
[Semana 1](../Semana%201/django_project) pero sin reutilizar ese repositorio.
Se creó el venv, se instaló Django 5.2.17, se ejecutó
`django-admin startproject config .` y luego `python manage.py startapp vet`.
Como esta App no usa base de datos, se eliminó la carpeta `vet/migrations/`
generada por defecto. Se registró `'vet'` en `INSTALLED_APPS` en
`src/config/settings.py`, se documentó `vet/apps.py` con
`verbose_name = 'Citas veterinaria'` (mismo estilo que `core` en Semana 1:
docstring + `verbose_name`), se creó `vet/urls.py` (vacío, listo para el
Ejercicio 6) y se conectó desde `config/urls.py` con `include('vet.urls')`.
También se preparó `templates/base.html` propio, sin nada de `core`. Se
verificó con `python manage.py check` que el proyecto no tiene errores.

**Comandos:**
```powershell
cd "Semana 2"
py -m venv django_project\venv
django_project\venv\Scripts\python.exe -m pip install "django==5.2.17"
cd django_project
mkdir src
cd src
..\venv\Scripts\python.exe -m django startproject config .
..\venv\Scripts\python.exe manage.py startapp vet
..\venv\Scripts\python.exe manage.py check
```

---

## Ejercicio 5 — Implementar el Model con datos estáticos

**Captura:** el archivo `vet/models.py` completo en VS Code.

**Explicación:** Como esta App no usa base de datos, en `vet/models.py` no se
definió un `models.Model` sino una clase Python simple `Cita` (con `mascota`,
`dueno`, `servicio`, `fecha`, `hora` y `estado`, este último con valor por
defecto `'Pendiente'`) y un método `__str__` para mostrarla de forma legible,
igual que se hizo con `Item` en Semana 1. Se creó la lista `citas` en memoria
con **5 registros de ejemplo**, usando `datetime.date` y `datetime.time` para
`fecha` y `hora` — los mismos tipos que usará el formulario del Ejercicio 7
(`DateField`/`TimeField`). Esta lista es la única fuente de datos de la
aplicación: no hay `makemigrations` ni `migrate` involucrados. Se verificó
cargando el módulo desde `manage.py shell`, confirmando que las 5 citas se
leen correctamente, y que `manage.py check` sigue sin errores.

**Comandos:**
```powershell
..\venv\Scripts\python.exe manage.py shell -c "from vet.models import citas; [print(c) for c in citas]"
..\venv\Scripts\python.exe manage.py check
```
