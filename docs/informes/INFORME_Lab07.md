# Informe — Laboratorio 07: ORM avanzado de Django

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Lucas Inga - Renzo Leon
**Repositorio:** https://github.com/RXDG2908/DesAplEmp-S02

En este laboratorio no se agregaron entidades nuevas: se aprovecharon las
relaciones de las semanas anteriores para registrar una operación de forma
segura, generar reportes, encapsular reglas del negocio y reducir el número de
consultas. Este informe cubre la **Parte 1 (app vet)**, que desarrolló Renzo
León. La Parte 2 (app biblioteca) corresponde a Lucas Inga.

## PARTE 1 — Consultas avanzadas sobre la app vet

### Ejercicio 1 — Recuperar la aplicación y ubicar sus campos clave

La entidad principal es la cita. Sus tres relaciones son la ficha clínica
(uno a uno), el veterinario (uno a muchos, la cita guarda la clave foránea) y
los insumos (muchos a muchos a través del modelo intermedio consumo de
insumo). Los tres campos que necesita el laboratorio son:

- Campo entero que se descuenta: el stock del insumo.
- Campo de estado: el estado de la cita (Pendiente, Confirmada o Atendida).
- Atributo numérico del modelo intermedio: la cantidad consumida, junto con el
  precio unitario.

Los tres ya existían desde las semanas anteriores, por lo que no fue necesario
crear una migración nueva; se comprobó que no hay cambios pendientes.

### Ejercicio 2 — Cargar datos de prueba

Se dejó un script de carga que se puede ejecutar varias veces sin duplicar
datos. La base quedó con 5 citas (estados Pendiente, Confirmada y Atendida),
3 veterinarios, 4 insumos y 8 consumos de insumo, cumpliendo el mínimo de la
guía (5, 3 y 8). Las citas y los veterinarios se revisaron en el listado del
Admin, y los consumos de cada cita se ven dentro de la pantalla de la cita.
Las citas de Luna y Toby quedaron con fecha de fines de octubre para que el
reporte tenga citas próximas.

### Ejercicio 3 — Registrar una operación con transacción y F()

Se creó la pantalla "Registrar consumo de insumo", con su ruta, su vista y una
plantilla que hereda de la plantilla base. Al enviar el formulario, la vista
hace tres cosas dentro de un solo bloque transaccional: registra el consumo,
marca la cita como Atendida y descuenta el stock del insumo. El descuento se
hace dentro de la base de datos con F(), y solo se aplica si el stock alcanza;
si no alcanza, se lanza un error que cancela todo el bloque y la plantilla
muestra el mensaje. Cuando todo sale bien se redirige al detalle de la cita
(patrón Post/Redirect/Get).

Se probaron dos casos con la jeringa de 5 ml, que empezó con stock 100:

- **Caso exitoso (cita de Toby, cantidad 2):** la página redirigió al detalle
  de la cita, que ya aparece como Atendida y con la jeringa en su lista de
  insumos. Los consumos pasaron de 8 a 9 y el stock bajó de 100 a 98.
- **Caso con falla (cita de Luna, cantidad 9999):** se mostró el mensaje
  "Stock insuficiente de Jeringa 5ml" en el mismo formulario. Antes y después
  había 5 citas, 9 consumos y 98 jeringas, y Luna siguió como Pendiente. Es
  decir, el consumo que se había creado primero y el cambio de estado también
  se deshicieron: ningún registro quedó a medias.

### Ejercicio 4 — Calcular un total con aggregate()

En el shell se calculó el total global consumido, sumando cantidad por precio
unitario de todos los consumos con F(). El resultado fue un diccionario con una
sola clave: el total es 110.50 soles.

aggregate() no devuelve un QuerySet porque resume toda la tabla en un único
valor. Un QuerySet es una colección de objetos del modelo; un total no es un
objeto ni una lista de ellos, así que Django devuelve un diccionario simple.
Por eso es una consulta final: no se le puede encadenar filter() ni
order_by().

### Ejercicio 5 — Calcular valores por objeto con annotate()

Con annotate() se agregó a cada cita el número de consumos que tiene, ordenado
de mayor a menor: Rocky 3, Luna 2, Toby 2, Michi 1 y Nala 1. A diferencia de
aggregate(), aquí el resultado sigue siendo un QuerySet de citas y cada cita
trae un valor calculado.

Con values() y annotate() se agruparon las citas por estado, también de mayor
a menor: Atendida 3, Pendiente 1 y Confirmada 1.

### Ejercicio 6 — Crear la página de reporte

Se creó la ruta de reporte, su vista y la plantilla del reporte, que hereda de
la plantilla base. Muestra el total global consumido, el número de consumos por
cita, las citas por estado y la cantidad de citas próximas pendientes. El total
global sale 110,50 soles y hay 1 cita próxima pendiente (la de Luna). El total
se muestra con el filtro de plantilla que fija dos decimales (floatformat), de
modo que siempre aparece con el formato de un precio.

### Ejercicio 7 — Crear un QuerySet personalizado

Se creó un QuerySet personalizado para la cita con dos métodos encadenables que
representan reglas del negocio: citas con un estado determinado y citas desde
hoy en adelante. Se asignó como manager de la cita con as_manager(). Se usa en
dos vistas: el listado de citas filtra por estado con el primer método, y el
reporte combina ambos para contar las citas próximas que siguen pendientes
(actualmente 1). El listado, el detalle y el filtro por estado siguen
respondiendo con normalidad, así que el CRUD de la Semana 3 no se rompió.

### Ejercicio 8 — Medir y optimizar el problema N+1

Con DEBUG activo se contaron las consultas con la lista de consultas de la
conexión, reiniciándola antes de cada medición. Con las 5 citas y los 9
consumos cargados:

| Pantalla | Sin optimizar | Optimizada |
|---|---|---|
| Listado con el veterinario de cada cita | 6 consultas | 1 consulta (select_related) |
| Citas con sus consumos e insumos | 15 consultas | 3 consultas (prefetch_related) |

Sin optimizar, Django hace una consulta para traer las citas y luego una más
por cada cita para llegar a su veterinario (6 = 1 + 5), y todavía más por cada
consumo al llegar a su insumo (15 = 1 + 5 + 9). Ese es el problema N+1: el número de consultas
crece con la cantidad de filas.

Cuándo usar cada método:

- **select_related()** se usa con relaciones de a uno (clave foránea o uno a
  uno): hace un JOIN y trae todo en una sola consulta.
- **prefetch_related()** se usa con relaciones de a muchos (muchos a muchos o
  la relación inversa de una clave foránea): hace una consulta por relación y
  une los resultados en Python, porque un JOIN repetiría las filas.

En la aplicación, el listado usa select_related() para el veterinario y la
ficha, y el detalle de la cita usa prefetch_related() para sus consumos y los
insumos de cada consumo.

## Conclusiones

- Registrar una operación que toca varios modelos dentro de una transacción
  evita datos a medias: si el stock no alcanza, nada se guarda. Descontar con
  F() hace la resta dentro de la base de datos y evita perder descuentos
  cuando dos ventas ocurren a la vez.
- aggregate() resume toda la tabla en un valor y annotate() calcula un valor
  por cada objeto o grupo; con ambos se armó el reporte sin escribir SQL.
- Un QuerySet personalizado concentra las reglas del negocio en un solo lugar
  y permite encadenarlas, en vez de repetir los mismos filtros en cada vista.
- Medir el número de consultas antes y después deja ver el problema N+1 con
  números: de 15 consultas se bajó a 3 y de 6 a 1.
