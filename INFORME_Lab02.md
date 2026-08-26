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

**Captura:** 4.png — la carpeta de la aplicación ya creada y registrada en la
configuración del proyecto.

**Explicación:** Esta aplicación se armó en su propio proyecto Django, dentro de
la carpeta de la Semana 2 y con su propio entorno virtual. Se tomó como guía la
estructura del laboratorio anterior, pero sin reutilizar ese proyecto. Primero se
creó el entorno virtual y se instaló Django, y después se generó el proyecto y,
dentro de él, la aplicación de citas. Como la aplicación no trabaja con base de
datos, se quitó la carpeta de migraciones que Django crea por defecto. Luego se
registró la aplicación en la configuración del proyecto, se le puso un nombre
descriptivo para identificarla fácil, y se dejó preparado su archivo de rutas
para conectarlo más adelante. También se creó una plantilla base propia. Al
final se revisó que el proyecto no tuviera errores.

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

**Capturas:**

- 5.png — el archivo del modelo abierto en el editor.
- 5b.png — la terminal mostrando las cinco citas de ejemplo.

**Explicación:** Como la aplicación no usa base de datos, aquí no se definió un
modelo de Django sino una clase de Python común y corriente para representar una
cita, con sus datos: la mascota, el dueño, el servicio, la fecha, la hora y el
estado. El estado arranca siempre como pendiente. También se le agregó una forma
de mostrarse en texto, para poder leerla fácil. Después se creó una lista con
cinco citas de ejemplo, que es la única fuente de datos de toda la aplicación.
No hay migraciones ni nada que se guarde en disco: si el servidor se reinicia,
la lista vuelve a su estado inicial. Para comprobar que todo estaba bien se
cargó la lista desde la consola de Django y se vieron las cinco citas, y se
revisó que el proyecto siguiera sin errores.

**Comandos:**
```powershell
..\venv\Scripts\python.exe manage.py shell -c "from vet.models import citas; [print(c) for c in citas]"
..\venv\Scripts\python.exe manage.py check
```

---

## Ejercicio 6 — Implementar el listado (View + URL + Template)

**Capturas:**

- 6.png — la vista que arma el listado.
- 6b.png — el archivo de rutas de la aplicación.
- 6c.png — la plantilla que muestra la tabla.
- 6d.png — el listado ya funcionando en el navegador.

**Explicación:** En este punto se completó el recorrido de la aplicación,
siguiendo el mismo camino del laboratorio anterior pero leyendo los datos de la
lista en memoria en vez de una base de datos. La vista toma las citas y las
ordena por fecha y por hora, para que se vean en el orden en que van a
atenderse y sea más fácil notar si dos se cruzan; el orden se hace sobre una
copia, así que la lista original no se toca. Esas citas ya ordenadas se le pasan
a la plantilla. Después se definió la ruta principal de la aplicación y se le
puso un nombre, de manera que el enlace de citas que ya estaba en la plantilla
base por fin funcione: antes no llevaba a ningún lado porque esa ruta todavía no
existía. Por último se armó la plantilla del listado, que hereda de la base y
recorre las citas mostrándolas en una tabla con sus seis datos. También
contempla el caso de que no haya ninguna cita, y muestra la fecha y la hora en
un formato cómodo de leer.

**Flujo verificado:** El navegador pide la página principal, el proyecto deriva
ese pedido a las rutas de la aplicación, la ruta llama a la vista, la vista lee
las citas de la lista en memoria y se las entrega a la plantilla, y la plantilla
arma la tabla que finalmente ve el usuario. Se comprobó que la página responde
correctamente, que se usan tanto la plantilla del listado como la plantilla
base, y que las cinco citas salen en el orden esperado: primero las del 26 de
agosto, de la más temprana a la más tardía, y después las del 27.

**Comandos:**
```powershell
..\venv\Scripts\python.exe manage.py check
..\venv\Scripts\python.exe manage.py runserver
```

- Listado de citas: http://127.0.0.1:8000/

**Casos de prueba:**

| # | Caso | Resultado esperado | Resultado obtenido |
|---|---|---|---|
| 1 | Abrir la página principal con las cinco citas de ejemplo | La página carga y muestra la tabla con cinco filas | Correcto |
| 2 | Orden de las filas | De la cita más próxima a la más lejana | Correcto |
| 3 | Herencia de plantilla | El listado se muestra dentro de la plantilla base, con su encabezado y su pie | Correcto |
| 4 | Enlace de citas de la barra de navegación | Lleva de vuelta al listado | Correcto |
| 5 | Formato de fecha y hora | Se leen como día, mes y año, y la hora en formato de 24 horas | Correcto |

> **Nota:** al levantar el servidor, Django crea un archivo de base de datos por
> las aplicaciones que trae de fábrica. La aplicación de citas no lo usa: sus
> datos siguen viviendo solamente en la lista en memoria. Ese archivo no forma
> parte de la entrega.

---

## Ejercicio 7 — Implementar el formulario

**Capturas:**

- 7.png — el archivo del formulario abierto en el editor.
- 7b.png — la terminal con las pruebas de validación.

**Explicación:** Se armó un formulario para registrar citas nuevas. Como la
aplicación no guarda nada en base de datos, el formulario se hizo desde cero en
vez de generarlo a partir de un modelo. Tiene un campo por cada dato que el
usuario debe llenar: la mascota, el dueño, el servicio, la fecha y la hora. El
estado no se pide, porque toda cita nueva entra como pendiente. El servicio no
se escribe a mano sino que se elige de una lista, que es la misma que ya estaba
definida junto a las citas, así no se inventan servicios que la veterinaria no
ofrece. La fecha y la hora usan los selectores propios del navegador, para que
sea más cómodo llenarlos y no haya dudas de formato.

Además se le agregó una revisión extra: antes de aceptar una cita, el
formulario comprueba que no haya ya otra agendada ese mismo día a esa misma
hora, y si la hay, avisa y no la deja pasar. Esto responde a uno de los
requisitos del inicio, el de evitar que dos citas se crucen en el mismo horario.
Por ahora el formulario solo valida; guardar la cita en la lista es lo que viene
en el siguiente ejercicio.

**Comandos:**
```powershell
..\venv\Scripts\python.exe manage.py check
```

**Casos de prueba:**

| # | Caso | Resultado esperado | Resultado obtenido |
|---|---|---|---|
| 1 | Todos los datos completos y con el horario libre | El formulario acepta la cita | Correcto |
| 2 | Una cita en un horario que ya está ocupado | Avisa que ese horario ya está tomado y no la acepta | Correcto |
| 3 | Dejar la mascota en blanco | Avisa que el campo es obligatorio | Correcto |
| 4 | Elegir un servicio que no está en la lista | Avisa que no es una opción válida | Correcto |
| 5 | Escribir una fecha que no existe en el calendario | Avisa que la fecha no es válida | Correcto |
