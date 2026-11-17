# Exposición — Laboratorio 11: comunicación entre componentes (cafetería y panel de Chamba PE)

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiante:** Renzo León
**Tema:** hacer que los componentes de React se comuniquen: el padre entrega
datos al hijo por props, el hijo avisa al padre con funciones recibidas por
props y, cuando dos hermanos necesitan el mismo dato, el estado se eleva al
padre. Se aplica primero en un mini catálogo con carrito (Parte 1) y después
en el panel administrativo del proyecto integrador **Chamba PE** (Parte 2).

> Todavía no se consume la API (Semana 12): los datos se escriben a mano con
> la misma forma que la respuesta de la API de la Semana 8 (los decimales
> como texto).

---

## De dónde partimos

En el Laboratorio 10 cada componente guardaba **su propio estado** y los
demás no se enteraban: el contador de [`InsumoCard`](../../frontend/src/components/InsumoCard.jsx) no lo veía nadie más. Ahora
los componentes necesitan **compartir** datos: el carrito tiene que saber qué
agregó el catálogo, y el resumen del panel tiene que saber qué eliminó una
fila.

```
Lab 10:  InsumoLista (estado)  →  InsumoCard (estado propio)       ← cada uno por su lado
Lab 11:  Practica (estado)     →  Catalogo → ProductoCard          ← un solo dueño del dato
                               →  Carrito                          ← el hermano lo ve
```

## Arquitectura: cómo funciona y para qué sirve

**Idea central.** Cada dato tiene **un solo dueño**: el componente padre que
contiene a todos los que lo necesitan. Los datos **bajan por props** y los
avisos **suben por funciones** que el padre entrega a los hijos.

```
Practica (estado: carrito, búsqueda, aviso)
 ├─ Buscador        ← baja: valor          · sube: onCambiar(texto)
 ├─ Catalogo        ← baja: productos visibles, onAgregar
 │    └─ ProductoCard × N                  · sube: onAgregar(producto)
 ├─ Carrito         ← baja: líneas         · sube: onQuitar(id), onVaciar()
 └─ Aviso           ← baja: mensaje        · sube: onTerminar('')
```

| Pieza | Para qué sirve | Archivo |
|---|---|---|
| **Props del padre al hijo** | Llevan datos de solo lectura hacia abajo | [`Catalogo`](../../frontend/src/practica/Catalogo.jsx), [`ProductoCard`](../../frontend/src/practica/ProductoCard.jsx) |
| **Función recibida por props** | El hijo **avisa** al padre (`onAgregar`, `onQuitar`, `onGuardar`) | [`ProductoCard`](../../frontend/src/practica/ProductoCard.jsx), [`Carrito`](../../frontend/src/practica/Carrito.jsx) |
| **Estado elevado** | El dato compartido vive en el padre común | [`Practica`](../../frontend/src/practica/Practica.jsx), [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) |
| **Datos derivados** | Lo que se calcula con el estado (total, conteos) **no** lleva `useState` | [`Carrito`](../../frontend/src/practica/Carrito.jsx), [`ResumenPrestadores`](../../frontend/src/components/ResumenPrestadores.jsx) |
| **Arreglos nuevos** | El estado se cambia con `map`, `filter` o *spread*, nunca con `push` ni `splice` | [`Practica`](../../frontend/src/practica/Practica.jsx) |
| **`useEffect`** | Código que corre **después** de dibujar, según su arreglo de dependencias | [`Carrito`](../../frontend/src/practica/Carrito.jsx), [`Aviso`](../../frontend/src/components/Aviso.jsx) |

**El flujo de datos, en una frase:** *los datos bajan por props, los avisos
suben por funciones y el estado vive en el único componente que ve a todos.*

1. [`Practica`](../../frontend/src/practica/Practica.jsx) guarda el carrito, el texto de búsqueda y el aviso con `useState`.
2. Filtra los productos con el texto y entrega la lista visible a `Catalogo` por **props**.
3. El usuario pulsa **Agregar** en un `ProductoCard` → la tarjeta llama a `onAgregar(producto)`, que es la función `agregarAlCarrito` del padre.
4. El padre crea un carrito **nuevo** (con `map` si el producto ya estaba, con *spread* si no) y React vuelve a dibujar.
5. `Carrito`, que es **hermano** de `Catalogo`, recibe las líneas nuevas por props y recalcula el total y las unidades con `reduce`.
6. El efecto de `Carrito` cambia el título de la pestaña y `Aviso` muestra el mensaje durante 3 segundos.

**Por qué se diseñó así:**

- **Un solo dueño por dato**: si el carrito viviera en `Catalogo`, el `Carrito` no podría leerlo, porque los hermanos no se ven entre sí.
- **Props de solo lectura**: el hijo no cambia el dato, **pide** el cambio; así el padre controla todo y la pantalla siempre se redibuja.
- **Sin estado duplicado**: el total se calcula a partir de las líneas; si se guardara aparte podría quedar distinto del carrito real.
- **Arreglos nuevos**: React detecta el cambio comparando referencias; un `push` modifica el mismo arreglo y la pantalla no se entera.
- **Limitación**: los datos siguen escritos a mano y se pierden al recargar; el siguiente paso es la API (Lab 12).

---

# PARTE 1 — Mini catálogo con carrito (`src/practica`)

## Paso 1 — Pasar datos del padre al hijo (Ejercicio 1)

En [`src/practica/datos.js`](../../frontend/src/practica/datos.js) hay cinco productos con el precio como texto, igual
que la API: Café americano (6.50), Capuchino (9.00), Torta de chocolate
(10.50), Jugo de naranja (7.00, stock 0) y Tostada (4.50). [`Practica`](../../frontend/src/practica/Practica.jsx) entrega los
productos a [`Catalogo`](../../frontend/src/practica/Catalogo.jsx) por props, y `Catalogo` entrega cada uno a [`ProductoCard`](../../frontend/src/practica/ProductoCard.jsx) con
`map()` y `key={producto.id}`. La tarjeta muestra el precio con
`Number(producto.precio).toFixed(2)` y **Agotado** cuando el stock es 0.

## Paso 2 — Tipos de props (Ejercicio 2)

| Prop | Tipo | La define | La lee |
|---|---|---|---|
| `productos` | arreglo | `Practica` | `Catalogo` |
| `producto` | objeto | `Catalogo` | `ProductoCard` |
| `onAgregar` | función | `Practica` | `Catalogo` → `ProductoCard` |
| `lineas` | arreglo | `Practica` | `Carrito` |
| `onQuitar`, `onVaciar` | función | `Practica` | `Carrito` |
| `valor` | texto | `Practica` | `Buscador` |
| `onCambiar` | función | `Practica` | `Buscador` |
| `mensaje` | texto | `Practica` | `Aviso` |
| `onTerminar` | función | `Practica` | `Aviso` |

**`ProductoCard` no puede modificar `producto`** porque el dato pertenece al
padre: la tarjeta solo lo recibe para mostrarlo, y si lo cambiara la pantalla
no se redibujaría. En Django pasa algo parecido con el **context** que una
View entrega al Template: el Template lo lee, pero quien lo cambia es la View.

## Paso 3 — Enlazar un evento con una función del padre (Ejercicio 3)

`ProductoCard` tiene un botón **Agregar**, desactivado con stock 0, que
ejecuta `onClick={() => onAgregar(producto)}`. Al principio
`agregarAlCarrito` solo hacía `console.log` del nombre: en la consola
aparecieron Capuchino y Café americano.

**El error de prueba:** al escribir `onClick={onAgregar(producto)}` la
pestaña se traba. La función se **ejecuta al dibujar** la tarjeta (no al hacer
clic), cambia el estado, React vuelve a dibujar, la función se ejecuta otra
vez… y así sin fin ("Too many re-renders"). Se corrige pasando una
**función flecha**, que React guarda y ejecuta solo con el clic.

## Paso 4 — Elevar el estado: el carrito compartido (Ejercicio 4)

El carrito vive en `Practica` como un arreglo de líneas
(`id`, `nombre`, `precio`, `cantidad`). En `agregarAlCarrito`:

- si el producto **ya está**, se aumenta su cantidad con `map()`;
- si **no está**, se agrega la línea con `[...carrito, nuevaLinea]` (sin `push`).

[`Carrito`](../../frontend/src/practica/Carrito.jsx) es **hermano** de `Catalogo` y recibe las líneas por props. **No
puede vivir en `ProductoCard` ni en `Catalogo`** porque esos componentes no
ven al `Carrito`; el único que ve a los dos es el padre.

## Paso 5 — Datos derivados (Ejercicio 5)

`Carrito` calcula con `reduce()` el total y las unidades, **sin** `useState`.
Prueba: dos Capuchinos y un Café americano → **3 unidades, S/ 24.50**
(2 × 9.00 + 6.50). El total no necesita su propio estado porque siempre se
puede calcular a partir de las líneas.

## Paso 6 — Quitar y vaciar desde el hijo (Ejercicio 6)

Cada línea tiene **Quitar** (`onQuitar(id)`) y hay un botón **Vaciar carrito**
(`onVaciar`). El padre usa `filter()` para quitar y `[]` para vaciar. Con el
carrito vacío se muestra **El carrito está vacío** con `&&`. No hay `push` ni
`splice` sobre el estado. Prueba: se quitó el Capuchino (quedó el Café
americano) y luego se vació todo.

## Paso 7 — Hermanos que comparten un filtro (Ejercicio 7)

[`Buscador`](../../frontend/src/practica/Buscador.jsx) recibe `valor` y `onCambiar`; el texto vive en `Practica`, que filtra
con `filter()` e `includes()` antes de entregar la lista a `Catalogo`. Con
"ca" aparecen Café americano y Capuchino; con "zzz", **No hay productos que
coincidan**. `Buscador` y `Catalogo` **no se hablan directamente**: el
buscador avisa al padre y el padre decide qué lista recibe el catálogo.

## Paso 8 — Ciclo de vida con `useEffect` (Ejercicio 8)

- En `Carrito`, un efecto con dependencia `[unidades]` cambia el título a
  `Carrito (3) · Cafetería` y escribe un `console.log`.
- [`Aviso`](../../frontend/src/components/Aviso.jsx) muestra **Agregado: \<nombre\>** y desaparece a los 3 segundos con
  `setTimeout`; el efecto **devuelve una función de limpieza** que cancela el
  temporizador.

| Arreglo de dependencias | Cuándo corre el efecto |
|---|---|
| `[]` | Una sola vez, al montar el componente |
| `[unidades]` | Al montar y cada vez que cambia `unidades` |
| Sin arreglo | Después de **cada** dibujo |

En desarrollo el mensaje aparece **dos veces** al montar porque
`React.StrictMode` (en [`main.jsx`](../../frontend/src/main.jsx)) monta, desmonta y vuelve a montar para
detectar efectos sin limpieza. `npm run lint` y `npm run build` terminan sin
errores.

---

# PARTE 2 — Panel administrativo de Chamba PE

**Chamba PE** conecta a clientes con prestadores de servicios verificados. La
entidad principal del panel es el **prestador**.

## Paso 9 — Identificar los componentes del panel (Ejercicio 9)

| En la práctica | En Chamba PE |
|---|---|
| Entidad principal | Prestador |
| Padre con el estado (`Practica`) | [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) |
| Catálogo + tarjeta | [`PrestadorListado`](../../frontend/src/components/PrestadorListado.jsx) + [`PrestadorFila`](../../frontend/src/components/PrestadorFila.jsx) (Aprobar, Suspender, Eliminar) |
| Formulario que avisa al padre | [`PrestadorForm`](../../frontend/src/components/PrestadorForm.jsx) con `onGuardar` |
| Carrito (resumen hermano) | [`ResumenPrestadores`](../../frontend/src/components/ResumenPrestadores.jsx): total, conteo por estado y tarifa promedio |
| Buscador | [`BuscadorPrestadores`](../../frontend/src/components/BuscadorPrestadores.jsx), por nombre |

```
PanelPrestadores (estado: prestadores, búsqueda, aviso)
 ├─ PrestadorForm          · sube: onGuardar(prestador)
 ├─ Aviso                  ← baja: mensaje        · sube: onTerminar
 ├─ BuscadorPrestadores    ← baja: valor          · sube: onCambiar
 ├─ PrestadorListado       ← baja: prestadores visibles
 │    └─ PrestadorFila × N · sube: aprobar, suspender, eliminar
 └─ ResumenPrestadores     ← baja: todos los prestadores
```

## Paso 10 — Estado elevado y listado (Ejercicio 10)

`PanelPrestadores` guarda en `useState` **seis prestadores** escritos a mano
con la forma de la API: `nombres`, `apellidos`, `rubro`, `tarifa` (como
texto) y `estado`. Los entrega a `PrestadorListado` por props, que dibuja una
`PrestadorFila` por prestador con `map()` y `key={prestador.id}`. Cada
componente está en su archivo de `src/components`.

## Paso 11 — Eventos enlazados en el listado (Ejercicio 11)

Cada fila tiene **Aprobar**, **Suspender** y **Eliminar**, que avisan al padre
con funciones recibidas por props; Aprobar y Suspender se desactivan si el
prestador ya está en ese estado. El padre usa `map()` para cambiar el estado y
`filter()` para eliminar.

Prueba: seis prestadores → María Torres pasa a **Aprobado** → Carlos Ramos
pasa a **Suspendido** → al eliminar a Jorge Medina quedan **cinco**. **La fila
no modifica la lista** porque solo recibe a su prestador como dato de
lectura; la lista es del padre.

## Paso 12 — Formulario de alta que avisa al padre (Ejercicio 12)

`PrestadorForm` es un formulario hijo con campos controlados (nombres,
apellidos, rubro y tarifa) que valida dos reglas: **nombres y apellidos
obligatorios** y **tarifa mayor que cero**. Si es válido, llama a
`onGuardar`; el padre lo agrega con un arreglo nuevo como **Pendiente** y los
campos quedan vacíos.

Pruebas: formulario vacío → error; tarifa 0 → error; **Pedro Soto Lima**,
Gasfitería, tarifa 45 → se agrega.

## Paso 13 — Resumen, buscador y `useEffect` (Ejercicio 13)

- `ResumenPrestadores` es hermano del listado y calcula el total, el conteo
  por estado y la tarifa promedio **sin** `useState`.
- `BuscadorPrestadores` está controlado por el padre: con "ro" aparecen Rosa
  Díaz y Pedro Soto; con "zzz", **No hay prestadores que coincidan**.
- Un efecto con `[prestadores.length]` cambia el título de la pestaña y el
  aviso de registro desaparece a los 3 segundos con su limpieza.

## Paso 14 — Verificar y publicar (Ejercicio 14)

La consola no muestra advertencias, `npm run lint` y `npm run build` terminan
sin errores, y `node_modules` y `dist` están en `.gitignore`. **El estado vive
en `PanelPrestadores`** porque es el único componente que ve a todos los
hermanos: el listado, el formulario y el resumen necesitan los mismos
prestadores, y así cualquier cambio se refleja a la vez en todas partes.

> **Nota:** el panel de citas de la veterinaria ([`PanelCitas`](../../frontend/src/components/PanelCitas.jsx)) fue la
> primera versión de esta Parte 2; la entrega final se hizo con Chamba PE. En
> el Lab 12 el panel pasó a leer la API y la regla de la tarifa quedó en el
> serializer (`validate_tarifa`).

## Resumen para el checklist

| Criterio | Dónde |
|---|---|
| Proyecto en `localhost:5173` y Parte 1 en `src/practica` | [`src/practica/`](../../frontend/src/practica/Practica.jsx) |
| Panel dividido en componentes (listado, fila, formulario, resumen) | `src/components/Prestador*.jsx`, [`ResumenPrestadores`](../../frontend/src/components/ResumenPrestadores.jsx) |
| Estado en un único padre, entregado por props | [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) |
| Botones de fila que avisan al padre | [`PrestadorFila`](../../frontend/src/components/PrestadorFila.jsx) |
| Formulario hijo controlado con validación y `onGuardar` | [`PrestadorForm`](../../frontend/src/components/PrestadorForm.jsx) |
| Arreglos nuevos (sin `push` ni `splice`) | `map`, `filter` y *spread* en el padre |
| Resumen hermano con datos derivados | [`ResumenPrestadores`](../../frontend/src/components/ResumenPrestadores.jsx) |
| Buscador controlado por el padre con mensaje vacío | [`BuscadorPrestadores`](../../frontend/src/components/BuscadorPrestadores.jsx), [`PrestadorListado`](../../frontend/src/components/PrestadorListado.jsx) |
| `useEffect` con dependencias y limpieza; lint y build sin errores | [`Aviso`](../../frontend/src/components/Aviso.jsx), [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx), Paso 14 |
