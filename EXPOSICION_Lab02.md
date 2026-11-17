# Exposición — Laboratorio 02: Nueva App `vet` con datos estáticos y formulario

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** crear desde cero una App Django para la reserva de citas de una
veterinaria, sin base de datos: los datos viven en una lista en memoria, y
se recorren con el flujo completo URL → View → Template, más un formulario
para registrar citas nuevas.

> Este documento explica, en el orden en que se hicieron, los diez
> ejercicios del Laboratorio 2. La idea es poder exponérselo al profesor
> contando la historia completa: qué problema se eligió, qué se construyó en
> cada paso y por qué, sin necesitar leer el código en paralelo.

---

## Conceptos clave (lectura rápida)

- **Project:** el sistema completo; guarda la **configuración** (`config/settings.py`, `config/urls.py`). Hay uno solo.
- **App:** un **módulo funcional** dentro del Project (aquí `vet`), con sus propias vistas, rutas y plantillas. Se **registra** en `INSTALLED_APPS`.
- **MVT (Model–View–Template):** el patrón de Django que separa **datos** (Model), **procesamiento** (View) y **presentación** (Template).
- **Model:** representa los **datos**. En esta semana es solo una **lista en memoria** (`citas`), sin base de datos.
- **View:** función que **recibe el Request**, decide qué hacer y **devuelve un Response** (normalmente con `render`).
- **URL (`urls.py`):** el **"director de tráfico"**: compara la dirección pedida con `path()` y llama a la View correcta.
- **Template:** archivo **HTML** con marcadores dinámicos: `{{ variable }}`, `{% for %}`, `{% if %}`.
- **Context:** el **diccionario** que la View le pasa al Template (`{'citas': citas}`).
- **Herencia de plantillas:** una plantilla hija usa **`{% extends 'base.html' %}`** y solo llena los **bloques** (`{% block content %}`); el encabezado y el menú se escriben **una sola vez** en `base.html`.
- **`forms.Form`:** formulario que **valida** los datos; **`clean()`** agrega reglas propias (aquí: **no dos citas a la misma hora**).
- **Post/Redirect/Get:** tras un **POST válido** se hace **`redirect`**; así, refrescar la página **no reenvía** el formulario.
- **Request → Response:** el recorrido siempre es **URL → View → Model → Template → Response**.

---

> **Enlaces al código:** los que dicen *(versión Lab 02)* abren en GitHub el
> código tal como quedó al terminar este laboratorio (commit `65c700c`),
> porque en semanas posteriores la lista en memoria se reemplazó por el ORM.
> Los demás abren el archivo local, que sigue vigente.

---

## De dónde partimos

En la Semana 1 se había trabajado sobre un proyecto ya armado (DjangoInicial,
con la App `core` y el modelo `Item`). En la Semana 2 la teoría fue
justamente explicar ese proyecto con el vocabulario de Django: Project vs.
App, el patrón MVT y el recorrido Request → Response.

El laboratorio pedía dar el siguiente paso: **construir una App propia**,
para una problemática real elegida por el equipo, pero todavía **sin base de
datos** — ni migraciones, ni Admin. La idea central es que el flujo MVT se
entiende igual aunque los datos estén en una lista de Python: la separación
entre datos, procesamiento y presentación no depende de que haya SQLite
detrás.

---

## Paso 1 — Elegir la problemática (Ejercicio 1)

Se eligió una **veterinaria de barrio** que recibe las citas por llamada o
mensaje, sin ningún registro centralizado. Eso provoca citas encimadas en el
mismo horario, solicitudes olvidadas y que no haya forma rápida de ver qué
horas del día ya están ocupadas. La aplicación la usarían el/la
recepcionista y el veterinario de turno.

---

## Paso 2 — Definir los requisitos funcionales (Ejercicio 2)

El laboratorio es en pareja y el profesor pidió **6 requisitos por
integrante**. Los seis de esta parte (Renzo) son los que se implementaron en
la App `vet`:

1. Registrar una nueva cita (mascota, dueño, servicio, fecha y hora).
2. Ver el listado de citas registradas.
3. Identificar el servicio solicitado (consulta, vacunación, cirugía, baño).
4. Distinguir el estado de la cita (pendiente, confirmada, atendida).
5. Ordenar las citas por fecha y hora, para que no se crucen dos en el mismo
   horario.
6. Identificar al dueño responsable de cada mascota, para contactarlo.

Los requisitos 7 a 12 (cancelar, ver detalle, asignar veterinario, filtrar,
buscar, contar por día) quedaron a cargo de Lucas Inga, que además hizo las
capturas y las pruebas del flujo.

---

## Paso 3 — Diseñar el modelo de datos (Ejercicio 3)

Una sola entidad, `Cita`, con seis campos. Cada uno está justificado por un
requisito:

| Campo | Tipo | Por qué existe |
|---|---|---|
| `mascota` | texto | Identifica al paciente (Req. 1) |
| `dueno` | texto | Permite contactar al responsable (Req. 1 y 6) |
| `servicio` | texto con opciones | Qué atención se brinda (Req. 3) |
| `fecha` | fecha | Ubica la cita en el calendario (Req. 5) |
| `hora` | hora | Evita cruces de horario (Req. 5) |
| `estado` | texto con opciones, por defecto *Pendiente* | Seguimiento (Req. 4) |

El estado no se le pide al usuario: toda cita nueva entra como pendiente.

---

## Paso 4 — Crear la App (Ejercicio 4)

**Ver en el código:** [config/settings.py — `INSTALLED_APPS` (L40)](django_project/src/config/settings.py#L40) · [config/urls.py — `include` (L22)](django_project/src/config/urls.py#L22) · [templates/base.html](django_project/src/templates/base.html)

Se armó un proyecto nuevo con su propio entorno virtual, tomando como guía
la estructura del laboratorio anterior pero sin reutilizarlo:

```powershell
py -m venv django_project\venv
django_project\venv\Scripts\python.exe -m pip install "django==5.2.17"
..\venv\Scripts\python.exe -m django startproject config .
..\venv\Scripts\python.exe manage.py startapp vet
```

Como la App no usa base de datos, se quitó la carpeta `migrations` que
Django genera por defecto. Se registró `vet` en `INSTALLED_APPS`, se dejó
preparado `vet/urls.py` y se creó la plantilla `base.html`. Al final se
corrió `manage.py check` para confirmar que el proyecto no tenía errores.

---

## Paso 5 — El Model con datos estáticos (Ejercicio 5)

**Ver en el código:** [vet/models.py — clase `Cita` (versión Lab 02) (L10)](https://github.com/RXDG2908/DesAplEmp-S02/blob/65c700cfe6ad91cc6a14e07a02d27a3e71b0d174/django_project/src/vet/models.py#L10) · [lista `citas` (versión Lab 02) (L26)](https://github.com/RXDG2908/DesAplEmp-S02/blob/65c700cfe6ad91cc6a14e07a02d27a3e71b0d174/django_project/src/vet/models.py#L26)

Aquí está la diferencia clave con un proyecto Django "normal": en
`vet/models.py` **no** se definió un `models.Model`, sino una clase de
Python común llamada `Cita`, con sus seis datos y un `__str__` para leerla
fácil. Debajo se creó una lista `citas` con cinco citas de ejemplo: esa
lista es la **única fuente de datos** de toda la App.

No hay nada guardado en disco: si el servidor se reinicia, la lista vuelve a
sus cinco citas iniciales. Se comprobó desde el shell:

```powershell
..\venv\Scripts\python.exe manage.py shell -c "from vet.models import citas; [print(c) for c in citas]"
```

---

## Paso 6 — El listado: View + URL + Template (Ejercicio 6)

**Ver en el código:** [vet/views.py — `cita_list` con `sorted` (versión Lab 02) (L8)](https://github.com/RXDG2908/DesAplEmp-S02/blob/65c700cfe6ad91cc6a14e07a02d27a3e71b0d174/django_project/src/vet/views.py#L8) · [vet/urls.py — `app_name` (L9)](django_project/src/vet/urls.py#L9) · [ruta `cita_list` (L14)](django_project/src/vet/urls.py#L14) · [templates/vet/cita_list.html — `extends` (L3)](django_project/src/templates/vet/cita_list.html#L3) · [`{% for %}` (L28)](django_project/src/templates/vet/cita_list.html#L28) · [`{% empty %}` (L42)](django_project/src/templates/vet/cita_list.html#L42)

Se completó el primer recorrido MVT:

- **View** (`cita_list` en `vet/views.py`): toma la lista y la ordena por
  fecha y hora con `sorted(...)`. El orden se hace sobre una copia, así que
  la lista original no se toca.
- **URL** (`vet/urls.py`): la ruta vacía `''` con el nombre `cita_list`, y
  `app_name = 'vet'` para poder escribir `vet:cita_list`. Con eso el enlace
  "Citas" que ya estaba en `base.html` por fin lleva a algún lado.
- **Template** (`cita_list.html`): hereda de `base.html` con `{% extends %}`,
  recorre las citas con `{% for %}` en una tabla de seis columnas, contempla
  el caso vacío con `{% empty %}` y formatea fecha y hora con los filtros
  `date` y `time`.

Se verificó en el navegador que las cinco citas salen ordenadas: primero las
del 26 de agosto, de la más temprana a la más tardía, y después las del 27.

---

## Paso 7 — El formulario (Ejercicio 7)

**Ver en el código:** [vet/forms.py — `CitaForm` (L9)](django_project/src/vet/forms.py#L9) · [`servicio` (ChoiceField) (L15)](django_project/src/vet/forms.py#L15) · [widgets de fecha y hora (L16)](django_project/src/vet/forms.py#L16) · [`clean()` (L26)](django_project/src/vet/forms.py#L26)

En `vet/forms.py` se creó `CitaForm` heredando de `forms.Form` (no de
`ModelForm`, porque no hay modelo de base de datos del cual generarlo). Tiene
un campo por cada dato que llena el usuario:

- `servicio` es un `ChoiceField` que toma sus opciones de la **misma lista**
  definida junto a las citas, así no se inventan servicios.
- `fecha` y `hora` usan los widgets `type="date"` y `type="time"`, para que el
  navegador muestre sus propios selectores.

Además se escribió un `clean()` propio: antes de aceptar la cita, revisa que
no exista otra con la misma fecha y hora, y si existe, lanza un error. Ese es
el Requisito 5 convertido en código.

---

## Paso 8 — La vista de creación (Ejercicio 8)

**Ver en el código:** [vet/views.py — `cita_crear` con `append` (versión Lab 02) (L14)](https://github.com/RXDG2908/DesAplEmp-S02/blob/65c700cfe6ad91cc6a14e07a02d27a3e71b0d174/django_project/src/vet/views.py#L14) · [redirect (versión Lab 02) (L31)](https://github.com/RXDG2908/DesAplEmp-S02/blob/65c700cfe6ad91cc6a14e07a02d27a3e71b0d174/django_project/src/vet/views.py#L31) · [ruta `nueva/` (L15)](django_project/src/vet/urls.py#L15) · [templates/vet/cita_form.html (L1)](django_project/src/templates/vet/cita_form.html#L1)

Se agregó la vista `cita_crear` y la ruta `nueva/`:

- En un **GET** muestra el formulario vacío.
- En un **POST** valida; si algo falla, vuelve a mostrar el formulario con
  el aviso y no guarda nada.
- Si todo está bien, arma una cita nueva con estado *Pendiente*, la agrega
  con `citas.append(...)` a la misma lista que usa el listado, deja un
  mensaje de confirmación y **redirige** al listado.

Ese redirect es el patrón **Post/Redirect/Get**: evita que al refrescar la
página se reenvíe el mismo POST. También se añadió "Nueva cita" en la barra
de navegación y la plantilla base quedó preparada para mostrar los mensajes.

---

## Paso 9 — Verificar el flujo completo (Ejercicio 9)

**Ver en el código:** [config/urls.py (L22)](django_project/src/config/urls.py#L22) · [vet/urls.py (L14)](django_project/src/vet/urls.py#L14)

Se recorrió la App de punta a punta: listado inicial con cinco citas →
formulario → registro de una cita en un horario libre → regreso al listado
con el aviso de confirmación, la cita nueva en su lugar y el total
actualizado.

| Paso | Qué ocurre |
|---|---|
| Request | El navegador pide `/nueva/` o envía el formulario |
| URL | `config/urls.py` deriva a `vet/urls.py`, que elige la vista |
| View | Muestra el formulario, o valida y agrega la cita a la lista |
| Model | La lista `citas` en memoria es la única fuente de datos |
| Template | `cita_list.html` o `cita_form.html`, ambos heredando de `base.html` |
| Response | El formulario, o el listado con la cita nueva |

Sobre cómo convive la App con otras: el Project es el contenedor único de
configuración y rutas; cada App tiene sus propias vistas, rutas y
plantillas, y se conecta registrándose en `INSTALLED_APPS` y enganchándose al
`urls.py` del proyecto. Se podría quitar una sin romper la otra.

---

## Paso 10 — Publicar en GitHub (Ejercicio 10)

**Ver en el código:** [requirements.txt](django_project/src/requirements.txt) · [django_project/README.md](django_project/README.md)

Se actualizó `requirements.txt` con `pip freeze`, se redactó el README con
la problemática, los requisitos, la estructura y cómo instalar y ejecutar, y
se subió todo al repositorio del equipo
(`github.com/RXDG2908/DesAplEmp-S02`). Se comprobó clonando en una carpeta
limpia que el proyecto se instala y arranca sin faltar nada.

---

## Cómo se verificó cada paso (resumen de pruebas)

| Paso | Qué se probó | Resultado |
|---|---|---|
| 4 | `manage.py check` sin errores | Correcto |
| 5 | El shell imprime las cinco citas de ejemplo | Correcto |
| 6 | El listado carga, ordenado y dentro de la plantilla base | Correcto |
| 7 | Horario ocupado, mascota vacía o fecha inválida son rechazados | Correcto |
| 8 | Una cita válida se guarda, redirige y aparece como Pendiente | Correcto |
| 8 | Reiniciar el servidor vuelve a las cinco citas iniciales | Correcto |
| 9 | Recorrido completo listado → formulario → listado | Correcto |
| 10 | Clonar en limpio, instalar y ejecutar | Correcto |

---

## Conclusión

El hilo conductor del laboratorio es que **el patrón MVT no depende de la
base de datos**: aquí el "Model" es solo una lista de Python, y aun así el
recorrido es el mismo que en cualquier proyecto Django — dirección, ruta,
vista, datos, plantilla y respuesta. El formulario es el punto donde un
requisito escrito en palabras ("que no se crucen dos citas") se vuelve una
regla que el sistema cumple. Y la limitación es deliberada: todo lo agregado
se pierde al reiniciar el servidor, que es exactamente el problema que se
resuelve en la Semana 3 con el ORM y SQLite.
