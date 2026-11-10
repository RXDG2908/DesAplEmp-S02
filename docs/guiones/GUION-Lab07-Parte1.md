# Guión expositivo — Laboratorio 7, Parte 1 (Veterinaria)

Guión para exponer en voz alta lo que se hizo en la parte del laboratorio
correspondiente a la aplicación de la veterinaria, indicando en qué archivo
está cada cosa.

## Introducción

"En este laboratorio no se creó ninguna entidad nueva. Se aprovecharon las
relaciones que ya teníamos desde la Semana 4 para cuatro cosas: registrar
una operación de forma segura con una transacción, sacar reportes con
`aggregate()` y `annotate()`, guardar las reglas del negocio en un QuerySet
propio y reducir el número de consultas a la base de datos. Casi todo está en
`vet/views.py` y `vet/models.py`."

## 1. Los campos clave

"La entidad principal es la cita, en `vet/models.py`. Tiene sus tres
relaciones: la ficha clínica uno a uno, el veterinario uno a muchos y los
insumos muchos a muchos a través del modelo intermedio `ConsumoInsumo`. Los
tres campos que pide la guía ya existían: `stock` en `Insumo`, que es el
número que se descuenta; `estado` en `Cita`, con Pendiente, Confirmada y
Atendida; y `cantidad` y `precio_unitario` en `ConsumoInsumo`. Por eso no
hubo migración nueva: `makemigrations --check` dice que no hay cambios."

## 2. Los datos de prueba

"Los datos se cargan con el script `cargar_lab07.py`, en la carpeta `src`.
Usa `get_or_create`, así que se puede ejecutar varias veces sin duplicar.
Deja 5 citas, 3 veterinarios, 4 insumos y 8 consumos, que es el mínimo de la
guía. Todo eso se puede ver en el Admin."

## 3. La transacción

"La pantalla Registrar consumo está en `/consumo/nuevo/`. Su vista es
`consumo_registrar`, en `vet/views.py`. Registrar un consumo toca tres
modelos: crea el consumo, pone la cita como Atendida y descuenta el stock
del insumo. Las tres cosas van dentro de `with transaction.atomic()`, así
que o se guarda todo o no se guarda nada.

El descuento se hace con `F('stock') - cantidad`, que hace la resta dentro de
la base de datos y no en Python, para que dos registros al mismo tiempo no se
pisen. Además el filtro `stock__gte=cantidad` hace que solo se descuente si
alcanza; si no alcanza, `update` devuelve cero filas y lanzamos un
`ValueError`. Ese error cancela todo el bloque y el Template
`consumo_form.html` muestra el mensaje. Si todo sale bien, se redirige al
detalle de la cita, que es el patrón Post/Redirect/Get.

Lo probamos con la jeringa, que tenía 100. Con Toby y 2 jeringas, los
consumos pasaron de 8 a 9 y el stock a 98. Con Luna y 9999 jeringas salió
'Stock insuficiente' y los números quedaron igual: 9 consumos, 98 de stock y
Luna siguió Pendiente. O sea, el rollback funcionó."

## 4. aggregate y annotate

"En el shell, con `aggregate()` y `Sum` de cantidad por precio, sale el total
consumido: 110.50 soles. `aggregate()` devuelve un diccionario y no un
QuerySet porque resume toda la tabla en un solo valor, por eso ya no se puede
seguir filtrando.

`annotate()`, en cambio, calcula un valor por cada objeto y sigue siendo un
QuerySet. Con `Count('consumos')` sacamos cuántos consumos tiene cada cita:
Rocky 3, Luna y Toby 2, Michi y Nala 1. Y con `values('estado')` más
`annotate` agrupamos por estado: Atendida 3, Pendiente 1 y Confirmada 1."

## 5. El reporte

"Todo eso se muestra en `/reporte/`. La vista `reporte` está al final de
`vet/views.py` y el Template es `templates/vet/reporte.html`, que hereda de
`base.html`. El total se muestra con el filtro `floatformat:2` para que salga
como precio, S/ 110,50. También muestra las citas próximas pendientes, que
es una. En el menú de `base.html` agregamos los enlaces a Registrar consumo y
a Reporte."

## 6. El QuerySet personalizado

"En `vet/models.py`, antes de la clase `Cita`, está `CitaQuerySet` con dos
métodos: `con_estado()`, que filtra por estado, y `proximas()`, que trae las
citas desde hoy. Se asigna en la cita con
`objects = CitaQuerySet.as_manager()`, y así se pueden usar desde
`Cita.objects` y encadenar. Se usa en dos vistas: `cita_list` filtra con
`con_estado()` cuando en la URL llega `?estado=Pendiente`, y el reporte hace
`proximas().con_estado('Pendiente').count()`. La ventaja es que la regla
está en un solo lugar. El listado, el detalle y el formulario siguen
funcionando igual."

## 7. El problema N+1

"Cuando un listado muestra datos de una relación, Django hace una consulta
para la lista y otra por cada fila. Lo medimos con el script `medir_n1.py`,
en `src`, que usa `reset_queries` y cuenta `connection.queries`. Para mostrar
el veterinario de cada cita eran 6 consultas, una más cinco; con
`select_related` bajó a 1. Para las citas con sus consumos e insumos eran 15;
con `prefetch_related` bajó a 3.

`select_related` sirve para relaciones de a uno, como la clave foránea o el
uno a uno, porque hace un JOIN. `prefetch_related` sirve para relaciones de a
muchos, porque hace una consulta aparte por relación y las une en Python. En
la app, `cita_list` usa `select_related` para el veterinario y la ficha, y
`cita_detalle` usa `prefetch_related` para los consumos."

## Cierre

"En resumen: la transacción evita datos a medias, `F()` evita perder
descuentos, `aggregate` y `annotate` arman el reporte sin escribir SQL, el
QuerySet propio guarda las reglas del negocio en un solo lugar y medir las
consultas mostró el N+1 con números, de 15 a 3. Y todo esto se reutilizó en
el Laboratorio 8: la API de citas filtra con `con_estado()` y su acción
`proximas` usa el mismo QuerySet."
