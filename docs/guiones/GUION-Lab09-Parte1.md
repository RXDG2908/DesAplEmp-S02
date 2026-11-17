# Guión expositivo — Laboratorio 9, Parte 1 (Veterinaria)

Guión para exponer en voz alta lo hecho con la veterinaria, indicando en qué
archivo está cada cosa.

## Introducción

"En este laboratorio pasamos del servidor al navegador. La app `vet` ya
entregaba JSON desde la API de la Semana 8; ahora hicimos una interfaz con
React y Vite. Todavía no consumimos la API: escribimos los datos a mano con
la misma forma que el JSON real. La interfaz está en [`frontend/src/Vet.jsx`](../../frontend/src/Vet.jsx),
y [`App.jsx`](../../frontend/src/App.jsx) la importa y la muestra."

## Arquitectura: cómo funciona y para qué sirve

"Primero la arquitectura. Hasta ahora el servidor armaba la página: Django usaba un Template y mandaba HTML listo. En este laboratorio cambia quién dibuja: lo hace el navegador, con JavaScript, usando React. Es una aplicación de una sola página. Django pasa a ser solo el proveedor de datos, con la API del laboratorio anterior.

Así funciona. Vite es el servidor de desarrollo y responde en el puerto 5173. El navegador pide la única página, [`index.html`](../../frontend/index.html), que tiene un `div` con id `root`. Esa página carga [`main.jsx`](../../frontend/src/main.jsx), que monta React dentro de ese `div`. React muestra el componente [`App.jsx`](../../frontend/src/App.jsx), y de ahí cuelga [`Vet.jsx`](../../frontend/src/Vet.jsx), que es la pantalla de la veterinaria. Ese componente devuelve JSX, que se parece a HTML pero vive dentro de JavaScript, y usa `map` para repetir un elemento por cada dato, como el `for` de los Templates, y condicionales para mostrar 'Sin stock' o 'Sin ficha clínica'.

Los datos salen por ahora de [`datos.js`](../../frontend/src/datos.js), escritos a mano pero con la misma forma que el JSON de la API. Eso es a propósito: más adelante se reemplazan por `fetch` sin rediseñar la pantalla. La ventaja de esta arquitectura es que la interfaz queda separada del servidor y se actualiza sin recargar la página. Lo que falta es justamente consumir la API y resolver CORS."

## 1. Entorno

"Instalamos Node.js, que con npm hace lo que Python con pip. El archivo
[`package.json`](../../frontend/package.json) cumple el papel de [`requirements.txt`](../../django_project/src/requirements.txt) y la carpeta
`node_modules` el de `venv`. En lugar de `runserver` usamos `npm run dev`,
que levanta http://localhost:5173/."

## 2. Estructura

"[`index.html`](../../frontend/index.html) es la única página y tiene un `div` con id `root`. [`main.jsx`](../../frontend/src/main.jsx)
monta React en ese `div`. [`App.jsx`](../../frontend/src/App.jsx) es el componente principal, y de ahí
cuelga [`Vet.jsx`](../../frontend/src/Vet.jsx). En Django, esto sería [`base.html`](../../django_project/src/templates/base.html), el punto de entrada y el
Template con su View."

## 3. JSX y expresiones

"En [`Vet.jsx`](../../frontend/src/Vet.jsx), el componente `Vet` devuelve JSX, que parece HTML pero es
JavaScript. Con llaves insertamos valores: el nombre de la aplicación, que es
una variable, y el precio de la consulta con IGV, que es un cálculo con
`toFixed(2)`. Da S/ 47.20."

## 4. Listas con map y key

"Los insumos son un arreglo de cinco objetos con id, nombre, unidad y stock.
Los recorremos con `map()` y a cada `li` le damos `key` igual al id, para que
React sepa cuál es cuál. Es el equivalente al `for` de los Templates de
Django."

## 5. Condicionales

"Si el stock es cero mostramos 'Sin stock' con un ternario; si es uno,
agregamos '¡Última unidad!' con `&&`. Si el arreglo está vacío mostramos 'No
hay registros'; lo probamos vaciándolo. En las citas, la ficha clínica puede
ser `null`, y en ese caso mostramos 'Sin ficha clínica'."

## 6. Relación anidada

"Cada cita trae sus consumos, que vienen de la relación muchos a muchos con
el modelo intermedio `ConsumoInsumo`. Hacemos un `map` de citas y, dentro, un
`map` de consumos, cada uno con su key. Con `reduce` sumamos los subtotales:
Firulais da 26.50 soles y Rocky 23.50."

## 7. Estilos y verificación

"Los estilos están en [`App.css`](../../frontend/src/App.css), con las clases `seccion-vet`, `sin-stock` y
`tarjeta-cita`, y un `style` en línea en los títulos. Ejecutamos `npm run
lint` y `npm run build` sin errores. `node_modules` y `dist` están en
`.gitignore`, así que no se suben."

## 8. Cierre

"La diferencia con los Templates es que allá el servidor entrega HTML
terminado, y acá el navegador arma la pantalla con JavaScript. Lo que falta
es consumir la API con `fetch` en la Semana 12, resolver CORS y reemplazar los
datos escritos a mano por la respuesta real."
