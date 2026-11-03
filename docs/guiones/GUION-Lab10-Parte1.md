# Guión expositivo — Laboratorio 10, Parte 1 (Veterinaria)

## Introducción

"En el laboratorio anterior toda la veterinaria estaba en un solo archivo,
`Vet.jsx`. Ahora la dividimos en componentes, que son funciones que reciben
datos por props, guardan lo que cambia en el estado y responden a eventos.
Los componentes están en `frontend/src/components` y los datos en
`src/datos.js`. Lo que en Django era un `include`, en React es un
componente."

## 1. Los componentes

"Hay cinco. `InsumoCard` muestra un insumo, `InsumoLista` muestra la lista,
`CitaCard` muestra una cita, `ConsumoItem` muestra un consumo y `Tarjeta` es
un contenedor. Todos tienen nombre en mayúscula y terminan en
`export default`; si el nombre fuera minúscula, React lo tomaría por una
etiqueta HTML."

## 2. Props y children

"`InsumoCard` recibe nombre, unidad y stock como props desestructuradas, y
`unidad` tiene un valor por defecto. `Tarjeta` recibe un título y `children`,
que es lo que va entre sus etiquetas; se parece al bloque de la herencia de
Templates de Django. `CitaCard` usa `Tarjeta` y dentro pone un `ConsumoItem`
por cada consumo, con `map` y `key`. Las props son de solo lectura: el hijo no
las modifica."

## 3. Estado y clic

"En `InsumoCard` hay un `useState` con el contador de reservados. El botón
Reservar llama a `setReservados` en el `onClick`. El contador solo se ve si
es mayor que cero, y el botón se desactiva si no hay stock. Cada tarjeta
tiene su propio contador. Una variable normal no serviría, porque React solo
redibuja cuando cambia el estado."

## 4. Búsqueda

"En `InsumoLista` el campo de búsqueda es controlado: su `value` viene del
estado y el `onChange` lo actualiza con `e.target.value`. La lista se filtra
sin distinguir mayúsculas. Si nada coincide, se muestra un mensaje. Probamos
'GASA', que da un resultado, y 'zzz', que muestra el mensaje."

## 5. Formulario

"El formulario tiene nombre y stock, también controlados, y usa `onSubmit`
con `preventDefault`. La regla viene de la API de la Semana 8: el stock debe
ser de al menos 1. Si no se cumple, aparece el error. Si se cumple, se crea
un arreglo nuevo con el operador spread, sin `push`, y se limpian los
campos."

## 6. Cierre

"Ejecutamos `npm run lint` y `npm run build` sin errores. Lo que falta es
guardar en la base de datos: ahora el insumo nuevo se pierde al recargar. En
la Semana 12 lo enviaremos con `fetch` a `/api/insumos/`, con CORS habilitado
en Django."
