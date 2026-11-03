# Exposición — Laboratorio 10, Parte 1: componentes, props, estado y eventos en la veterinaria (`vet`)

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** reorganizar la interfaz React de la veterinaria en componentes
reutilizables que reciben datos por props, y agregarle estado (`useState`) y
eventos (`onClick`, `onChange`, `onSubmit`).

> Todavía no se consume la API (Semana 12) ni se pasan funciones entre
> componentes (Semana 11): el estado y los eventos viven dentro del
> componente que los usa.

---

## De dónde partimos

En el Laboratorio 9, `Vet.jsx` hacía todo en un solo componente: tenía los
arreglos escritos a mano, recorría insumos y citas, y calculaba los totales.
Ahora esa misma interfaz se divide en piezas. Lo que en Django era un
`{% include %}` con datos del context, en React es un componente con props.

```
main.jsx → App.jsx → Vet.jsx → InsumoLista → InsumoCard
                            → CitaCard → Tarjeta (children)
                                       → ConsumoItem
```

## Paso 1 — Identificar los componentes (Ejercicio 1)

Se movieron los datos a `src/datos.js` y se crearon los archivos en
`src/components/`. Tres candidatos de `Vet.jsx`:

| Fragmento | Componente | Por qué |
|---|---|---|
| Un `<li>` de insumo | `InsumoCard` | Se repite por cada insumo |
| El bloque de una cita | `CitaCard` | Se repite y tiene su propia relación anidada |
| Un consumo dentro de la cita | `ConsumoItem` | Elemento de la relación N:M |

## Paso 2 — Primer componente funcional (Ejercicio 2)

`InsumoCard.jsx` es una función con nombre en mayúscula que devuelve JSX y
termina en `export default`. En `Vet.jsx` se importa y se usa como
`<InsumoCard />`. **Si el nombre fuera minúscula** (`<insumoCard />`) React lo
tomaría como una etiqueta HTML normal, no como un componente, y no mostraría
nada útil.

## Paso 3 — Props y lista (Ejercicio 3)

`InsumoCard({ nombre, unidad = 'unidad', stock })` recibe las props
desestructuradas, y `unidad` tiene un valor por defecto. `InsumoLista` recibe
el arreglo y lo muestra con `map()` y `key={insumo.id}`.

## Paso 4 — Contenedor con `children` (Ejercicio 4)

`Tarjeta({ titulo, children })` dibuja el marco y el título, y coloca lo que
se escribe entre sus etiquetas. `CitaCard` la usa para envolver los datos de
cada cita. **`children` equivale al `{% block %}` de la herencia de Templates
de la Semana 6** (el hueco que rellena el hijo) y también a lo que un
`{% include %}` recibiría.

## Paso 5 — Componentes dentro de componentes: 1:N (Ejercicio 5)

`CitaCard` muestra los consumos con un `ConsumoItem` por cada uno y calcula
el total con `reduce`. El campo de la API `dueno` se recibe como
`propietario` (`dueno: propietario`). **Un componente no debe modificar sus
props** porque son solo lectura: el dato pertenece al padre, y cambiarlo no
redibuja la pantalla. Al intentarlo (`props.cantidad = 99`), ESLint marca
"Modifying component props or hook arguments is not allowed".

## Paso 6 — Estado y evento de clic (Ejercicio 6)

`InsumoCard` tiene `const [reservados, setReservados] = useState(0)` y un
botón **Reservar** con `onClick`. El contador solo aparece si es mayor que
cero (`reservados > 0 && …`) y el botón se desactiva cuando `stock === 0` o
ya se reservó todo el stock. Cada tarjeta tiene su propio estado: reservar un
suero no cambia a las demás. Una variable `let` no actualiza la pantalla
porque React solo vuelve a dibujar el componente cuando cambia el estado.

Prueba hecha: el Suero fisiológico (stock 1) se reserva una vez y el botón
queda desactivado; el Antiparasitario (stock 0) nace desactivado.

## Paso 7 — Campo controlado que filtra (Ejercicio 7)

En `InsumoLista` el campo de búsqueda es controlado:
`value={busqueda}` y `onChange={(e) => setBusqueda(e.target.value)}`. La
lista visible es `insumos.filter(i => i.nombre.toLowerCase().includes(busqueda.toLowerCase()))`.
Búsquedas probadas: "GASA" → 1 resultado (Gasa estéril); "zzz" → mensaje
"Ningún insumo coincide con la búsqueda".

## Paso 8 — Formulario controlado con validación (Ejercicio 8)

El formulario tiene nombre y stock, ambos controlados, y usa `onSubmit` con
`e.preventDefault()`. La regla viene de la API de la Semana 8
(`validate_stock`): **el stock inicial debe ser de al menos 1**. Si no se
cumple, se muestra "El stock inicial debe ser de al menos 1 unidad." Si es
válido, se agrega con un arreglo nuevo (`setInsumos([...insumos, nuevo])`,
sin `push`) y se limpian los campos.

Prueba hecha: Venda con stock 0 → error y la lista queda en 5; Venda con
stock 5 → se agrega y la lista pasa a 6, sin error.

`npm run lint` y `npm run build` terminan sin errores.

**Qué falta para guardar en la base de datos de Django:** el registro nuevo
vive solo en la memoria del navegador y se pierde al recargar. Hay que
enviarlo con `fetch` (POST a `/api/insumos/`), habilitar CORS en Django y
manejar la respuesta o los errores de la API (Semana 12).

## Resumen para el checklist

| Criterio | Dónde |
|---|---|
| 3+ componentes en `src/components`, nombre en mayúscula | `InsumoCard`, `InsumoLista`, `CitaCard`, `ConsumoItem`, `Tarjeta` |
| Props desestructuradas + valor por defecto / `children` | `unidad = 'unidad'`, `Tarjeta` |
| Lista con `map()` y `key` | `InsumoLista`, `CitaCard` |
| Relación 1:N con componente dentro de componente | `CitaCard` → `ConsumoItem` |
| `useState` + `onClick` | `InsumoCard` |
| Campo controlado que filtra | `InsumoLista` |
| Formulario con `onSubmit`, `preventDefault` y validación | `InsumoLista` |
| Lint y build sin errores | Paso 8 |
| Qué resuelven props y estado | Props llevan datos del padre al hijo; el estado guarda lo que cambia y redibuja |
