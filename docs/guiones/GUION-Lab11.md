# Guión expositivo — Laboratorio 11 (Cafetería y panel de Chamba PE)

## Introducción

"En el laboratorio anterior cada componente guardaba su propio estado y los
demás no se enteraban de lo que pasaba en él. En este laboratorio los
componentes se comunican: el padre le pasa datos al hijo por props, el hijo
le avisa al padre con funciones que recibe por props y, cuando dos hermanos
necesitan el mismo dato, ese dato sube al padre. Primero lo practicamos con
una cafetería en `src/practica` y después lo aplicamos en el panel de mi
proyecto integrador, Chamba PE. Todavía no usamos la API: los datos están
escritos a mano, con la misma forma que la respuesta de la Semana 8."

## Arquitectura: cómo funciona y para qué sirve

"La regla de este laboratorio es que cada dato tiene un solo dueño, que es el
componente padre que contiene a todos los que lo necesitan. Los datos bajan
por props y los avisos suben por funciones.

En la cafetería, el dueño es [`Practica`](../../frontend/src/practica/Practica.jsx). Guarda el carrito, el texto del
buscador y el aviso. A [`Catalogo`](../../frontend/src/practica/Catalogo.jsx) le pasa los productos, y [`Catalogo`](../../frontend/src/practica/Catalogo.jsx) le pasa cada
uno a [`ProductoCard`](../../frontend/src/practica/ProductoCard.jsx). Cuando pulso Agregar, la tarjeta no toca el carrito: llama
a la función `onAgregar` que le pasó el padre. El padre arma un carrito nuevo,
React vuelve a dibujar y el [`Carrito`](../../frontend/src/practica/Carrito.jsx), que es hermano del catálogo, recibe las
líneas actualizadas.

Por qué el carrito vive en el padre: porque el catálogo y el carrito no se ven
entre sí. El único que ve a los dos es [`Practica`](../../frontend/src/practica/Practica.jsx). Y el total no tiene su propio
estado, porque se puede calcular siempre con las líneas; si lo guardara
aparte, podría quedar distinto del carrito real. La limitación es que todo
sigue en memoria y se pierde al recargar; eso lo resuelve la API en el
próximo laboratorio."

## 1. Datos del padre al hijo

"En `src/practica` tengo cinco productos con el precio como texto, igual que
la API. [`Practica`](../../frontend/src/practica/Practica.jsx) se los pasa a [`Catalogo`](../../frontend/src/practica/Catalogo.jsx), y [`Catalogo`](../../frontend/src/practica/Catalogo.jsx) dibuja un
[`ProductoCard`](../../frontend/src/practica/ProductoCard.jsx) por producto con `map` y una `key` con el id. La tarjeta muestra
el precio con dos decimales y la palabra Agotado cuando el stock es cero,
como en el jugo de naranja.

La tarjeta no puede cambiar la prop `producto`, porque es del padre. Es como
el context de Django: el Template lo lee, pero el que lo cambia es la View."

## 2. El evento que avisa al padre

"La tarjeta tiene un botón Agregar que llama a `onAgregar` con el producto.
Lo escribo con una función flecha. Si escribo `onAgregar(producto)` sin la
flecha, la función se ejecuta al dibujar, cambia el estado, React vuelve a
dibujar y se repite sin fin; por eso la pestaña se trabó en la prueba. Con la
flecha, React guarda la función y la ejecuta solo con el clic."

## 3. El estado elevado y los datos derivados

"El carrito vive en [`Practica`](../../frontend/src/practica/Practica.jsx). Si el producto ya está, aumento la cantidad
con `map`; si no está, creo un arreglo nuevo con el operador spread. Nunca
uso `push`. El [`Carrito`](../../frontend/src/practica/Carrito.jsx) calcula el total y las unidades con `reduce`. Agregué
dos capuchinos y un café americano: tres unidades y un total de veinticuatro
soles con cincuenta. Para quitar uso `filter` y para vaciar, un arreglo
vacío."

## 4. El buscador compartido

"El [`Buscador`](../../frontend/src/practica/Buscador.jsx) recibe el valor y una función `onCambiar`. El texto se guarda
en el padre, que filtra los productos antes de dárselos al catálogo. Con 'ca'
aparecen el café americano y el capuchino; con 'zzz' sale el mensaje de que
no hay coincidencias. El buscador y el catálogo no se hablan: los dos pasan
por el padre."

## 5. useEffect y la limpieza

"En el [`Carrito`](../../frontend/src/practica/Carrito.jsx), un efecto cambia el título de la pestaña cada vez que cambian
las unidades. El [`Aviso`](../../frontend/src/components/Aviso.jsx) muestra 'Agregado' y desaparece a los tres segundos con
un temporizador; el efecto devuelve una función que cancela ese temporizador.
Con un arreglo vacío el efecto corre una vez; con una dependencia, cada vez
que cambia; sin arreglo, en cada dibujo. En desarrollo el mensaje sale dos
veces porque `StrictMode` monta el componente dos veces para encontrar
efectos sin limpieza."

## 6. El panel de Chamba PE

"Ahora lo mismo en mi proyecto. Chamba PE conecta a clientes con prestadores
de servicios verificados, y la entidad del panel es el prestador. El padre es
[`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx), que guarda seis prestadores. Contiene al formulario, al aviso,
al buscador, al listado con sus filas y al resumen.

Cada fila tiene Aprobar, Suspender y Eliminar, que avisan al padre. Aprobé a
María Torres, suspendí a Carlos Ramos y eliminé a Jorge Medina: quedaron
cinco. La fila no cambia la lista, solo le avisa al padre, que usa `map` o
`filter`.

El formulario valida que los nombres y apellidos no estén vacíos y que la
tarifa sea mayor que cero. Registré a Pedro Soto Lima con una tarifa de
cuarenta y cinco y apareció como pendiente.

El resumen calcula el total, el conteo por estado y la tarifa promedio sin
estado propio. El buscador con 'ro' muestra a Rosa Díaz y a Pedro Soto, y
con 'zzz' muestra el mensaje. Y un efecto pone en la pestaña la cantidad de
prestadores."

## 7. Cierre

"La consola no muestra advertencias y `npm run lint` y `npm run build`
terminan sin errores. El estado vive en [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) porque es el único que
ve a todos los hermanos: así un cambio en una fila se ve a la vez en el
listado y en el resumen. Lo que falta es que los datos dejen de estar escritos
a mano: en el Laboratorio 12 el panel los pide a la API de Django."
