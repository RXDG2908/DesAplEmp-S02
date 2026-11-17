# Guión expositivo — Laboratorio 10, Parte 1 (Veterinaria)

## Introducción

"En el laboratorio anterior toda la veterinaria estaba en un solo archivo,
[`Vet.jsx`](../../frontend/src/Vet.jsx). Ahora la dividimos en componentes, que son funciones que reciben
datos por props, guardan lo que cambia en el estado y responden a eventos.
Los componentes están en `frontend/src/components` y los datos en
[`src/datos.js`](../../frontend/src/datos.js). Lo que en Django era un `include`, en React es un
componente."

## Arquitectura: cómo funciona y para qué sirve

"La arquitectura de este laboratorio es de componentes. En el anterior toda la pantalla estaba en un solo archivo, [`Vet.jsx`](../../frontend/src/Vet.jsx). Ahora está dividida en piezas pequeñas que se combinan: es la misma idea del `include` y del `block` de Django, pero con datos y comportamiento incluidos.

El árbol es así. [`Vet.jsx`](../../frontend/src/Vet.jsx) contiene a [`InsumoLista`](../../frontend/src/components/InsumoLista.jsx), que muestra varios [`InsumoCard`](../../frontend/src/components/InsumoCard.jsx), y contiene varios [`CitaCard`](../../frontend/src/components/CitaCard.jsx), cada uno dentro de un [`Tarjeta`](../../frontend/src/components/Tarjeta.jsx) con varios [`ConsumoItem`](../../frontend/src/components/ConsumoItem.jsx). Y todo se mueve con una regla: los datos bajan por props, los cambios se guardan en el estado y los eventos disparan esos cambios.

Lo explico con un caso. [`Vet.jsx`](../../frontend/src/Vet.jsx) toma los datos de [`datos.js`](../../frontend/src/datos.js) y se los pasa a los hijos por props, que son de solo lectura. [`InsumoLista`](../../frontend/src/components/InsumoLista.jsx) guarda en su estado la lista, la búsqueda y el formulario. Cuando escribo en el buscador, el evento `onChange` actualiza el estado y React vuelve a dibujar solo la lista filtrada. Cuando pulso Reservar en un [`InsumoCard`](../../frontend/src/components/InsumoCard.jsx), `onClick` suma uno al contador de esa tarjeta, y las demás no se enteran. Cuando envío el formulario, `onSubmit` con `preventDefault` evita recargar la página, valida que el stock sea al menos uno, igual que la API, y crea un arreglo nuevo con la lista más el insumo.

Se usa `useState` y no una variable normal porque React solo redibuja cuando cambia el estado. La limitación es que el insumo nuevo vive solo en memoria y se pierde al recargar; guardarlo en la base es el siguiente paso, con `fetch` a la API."

## 1. Los componentes

"Hay cinco. [`InsumoCard`](../../frontend/src/components/InsumoCard.jsx) muestra un insumo, [`InsumoLista`](../../frontend/src/components/InsumoLista.jsx) muestra la lista,
[`CitaCard`](../../frontend/src/components/CitaCard.jsx) muestra una cita, [`ConsumoItem`](../../frontend/src/components/ConsumoItem.jsx) muestra un consumo y [`Tarjeta`](../../frontend/src/components/Tarjeta.jsx) es
un contenedor. Todos tienen nombre en mayúscula y terminan en
`export default`; si el nombre fuera minúscula, React lo tomaría por una
etiqueta HTML."

## 2. Props y children

"[`InsumoCard`](../../frontend/src/components/InsumoCard.jsx) recibe nombre, unidad y stock como props desestructuradas, y
`unidad` tiene un valor por defecto. [`Tarjeta`](../../frontend/src/components/Tarjeta.jsx) recibe un título y `children`,
que es lo que va entre sus etiquetas; se parece al bloque de la herencia de
Templates de Django. [`CitaCard`](../../frontend/src/components/CitaCard.jsx) usa [`Tarjeta`](../../frontend/src/components/Tarjeta.jsx) y dentro pone un [`ConsumoItem`](../../frontend/src/components/ConsumoItem.jsx)
por cada consumo, con `map` y `key`. Las props son de solo lectura: el hijo no
las modifica."

## 3. Estado y clic

"En [`InsumoCard`](../../frontend/src/components/InsumoCard.jsx) hay un `useState` con el contador de reservados. El botón
Reservar llama a `setReservados` en el `onClick`. El contador solo se ve si
es mayor que cero, y el botón se desactiva si no hay stock. Cada tarjeta
tiene su propio contador. Una variable normal no serviría, porque React solo
redibuja cuando cambia el estado."

## 4. Búsqueda

"En [`InsumoLista`](../../frontend/src/components/InsumoLista.jsx) el campo de búsqueda es controlado: su `value` viene del
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
