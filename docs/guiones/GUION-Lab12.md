# Guión expositivo — Laboratorio 12 (Insumos y panel de Chamba PE con la API)

## Introducción

"Hasta el laboratorio anterior, React trabajaba con datos escritos a mano y
todo se perdía al recargar. En este laboratorio React se conecta con Django:
pide los datos a la API con una petición Ajax, los muestra sin recargar la
página y envía los cambios con POST, PATCH y DELETE. Son dos aplicaciones
distintas que corren a la vez: Django en el puerto 8000 y React en el 5173.
Primero lo practico con los insumos de la veterinaria y después con el panel
de mi proyecto integrador, Chamba PE."

## Arquitectura: cómo funciona y para qué sirve

"La idea principal es que React no reemplaza a Django. Django entrega y
valida los datos con el serializer y el ViewSet; React los pide, los dibuja y
manda los cambios.

El recorrido de una petición es así. React decide cuándo pedir los datos.
Axios envía la petición HTTP. El ViewSet recibe la petición y decide qué
operación hacer. El serializer valida lo que llega y lo convierte a JSON. Y
el ORM habla con la base SQLite. La respuesta vuelve con un código: 200 si
todo salió bien, 201 al crear, 204 al eliminar, 400 si los datos no cumplen
una regla y 404 si el registro no existe.

Lo explico con un caso. [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) se dibuja mostrando 'Cargando'. Su
efecto pide la lista a la API. Cuando llega, una función adaptadora convierte
la tarifa, que viene como texto, a número, y la guardo en el estado. Si
registro un prestador, el formulario manda un POST; si la API responde 201,
lo agrego a la lista; si responde 400, muestro el mensaje del serializer. El
estado cambia solo cuando la API responde bien, así la pantalla muestra lo
que de verdad quedó guardado.

La limitación es que la API todavía está abierta a cualquiera: falta la
autenticación y los permisos."

## 1. La API y CORS

"Con Django encendido, la dirección `/api/insumos/` responde 200 con la lista
en JSON. A diferencia de un Template, la API no entrega una página, solo los
datos y un código.

Cuando hice un fetch desde React, el navegador lo bloqueó por CORS. Para el
navegador, otro puerto es otro origen, y no deja leer datos de otro origen si
el servidor no lo autoriza. Instalé `django-cors-headers`, lo agregué a las
aplicaciones, puse su middleware arriba de todo y autoricé
`localhost:5173`. Al repetir, respondió 200."

## 2. Axios y la instancia

"Instalé Axios y creé [`api.js`](../../frontend/src/api.js) con `axios.create`, una `baseURL` y un
`timeout`. La dirección del servidor se escribe una sola vez; los
componentes solo usan rutas cortas. Si mañana cambia el servidor, cambio una
línea."

## 3. GET y los tres estados

"En [`ListaPractica`](../../frontend/src/practica/ListaPractica.jsx) pido los insumos dentro de un `useEffect`. Va en un efecto
porque el cuerpo del componente se ejecuta en cada dibujo: si la petición
estuviera ahí, cada respuesta haría otro dibujo y otra petición, sin parar. Y
la función del efecto no es `async`, porque un efecto solo puede devolver una
función de limpieza; por eso declaro `cargar` adentro y la llamo.

Con `try`, `catch` y `finally` manejo tres estados: 'Cargando' mientras
espera, 'No se pudo cargar la lista' si apago Django, y 'No hay insumos
registrados' si llega vacía. La pantalla nunca queda en blanco."

## 4. POST, PATCH y DELETE

"El formulario crea un insumo con POST y responde 201. Si mando stock cero,
la API responde 400 y muestro el mensaje de la regla de la Semana 8: el stock
inicial debe ser de al menos una unidad. El botón Eliminar manda DELETE y,
con el 204, lo quito con `filter`. El botón más uno manda PATCH y, con el
200, lo reemplazo con `map`. El buscador manda el texto como `?search=` y la
lista se vuelve a pedir cada vez que cambia."

## 5. El panel de Chamba PE

"Mi API no tenía prestadores, así que antes agregué la app `chamba` al
proyecto: el modelo Prestador, el serializer con `validate_tarifa`, que exige
una tarifa mayor que cero, un ModelViewSet con búsqueda, filtro por estado y
orden, y la ruta `/api/chamba/prestadores/`. Los seis prestadores se cargan
con un script.

En el panel cambié los datos a mano por un GET en un efecto. Para crear,
mando un POST: registré a Pedro Soto y respondió 201. Con tarifa cero
respondió 400 y el mensaje apareció junto al formulario. Para editar, el
botón Editar llena el formulario con los datos de la fila y al guardar manda
un PATCH: cambié a Pedro a tarifa cuarenta y ocho y rubro Electricidad, con
200. Aprobar y suspender también son PATCH."

## 6. Eliminar con confirmación y los filtros

"Eliminar pide confirmación: el primer clic cambia el botón a Confirmar y
solo el segundo manda el DELETE. Con 204 lo quito de la lista. Si responde
404, porque alguien ya lo borró, aviso y también lo quito. Lo probé borrando
un prestador directo en la API y luego desde la pantalla. En Network se ve
antes una petición OPTIONS, que es la consulta previa de CORS.

El buscador y el filtro por estado viajan como `?search=` y `?estado=`. Con
'ro' salen Rosa Díaz y Pedro Soto; con 'Aprobado' solo los aprobados; y se
pueden combinar con el símbolo &. El resumen calcula el total, el conteo y el
promedio con lo que llega de la API. Además, la limpieza del efecto cancela
la petición anterior con `AbortController`."

## 7. Cierre

"La consola no muestra advertencias, Django no muestra errores 500 y
`npm run lint` y `npm run build` terminan sin errores. Lo que resuelve Ajax es
que el panel se actualiza sin recargar la página: React pide solo los datos y
Django valida y guarda. Lo que falta es la autenticación y los permisos: hoy
cualquiera que conozca la dirección puede modificar los prestadores, y ese
panel solo debería usarlo el administrador de Chamba PE."
