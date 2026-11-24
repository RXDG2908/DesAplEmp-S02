// ==================================================================
// ARCHIVO  : practica/Carrito.jsx
// PARTE 1  : práctica del Lab 11 (mini catálogo con carrito: CAFETERÍA)
// ROL      : HERMANO de Catalogo; muestra las líneas que recibe por props.
// ------------------------------------------------------------------
// LAB 11 - EJ 4: recibe las LÍNEAS del carrito por props (el estado está en el padre).
// LAB 11 - EJ 5: TOTAL y UNIDADES con reduce(), SIN useState (DATOS DERIVADOS).
// LAB 11 - EJ 6: botones Quitar (onQuitar(id)) y Vaciar (onVaciar) AVISAN AL PADRE;
//                'El carrito está vacío' se muestra con &&.
// LAB 11 - EJ 8: useEffect con [unidades] cambia el TÍTULO DE LA PESTAÑA.
// ------------------------------------------------------------------
// USADO EN : ./Practica.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 4 .... línea 40
//   LAB 11 - EJ 5 .... línea 23
//   LAB 11 - EJ 6 .... línea 43
//   LAB 11 - EJ 8 .... línea 27
// ==================================================================
import { useEffect } from 'react'

function Carrito({ lineas, onQuitar, onVaciar }) {
  // LAB 11 - EJ 5: DATOS DERIVADOS -> se calculan en cada dibujo; no necesitan su propio estado.
  const total = lineas.reduce((suma, l) => suma + Number(l.precio) * l.cantidad, 0)
  const unidades = lineas.reduce((suma, l) => suma + l.cantidad, 0)

  // LAB 11 - EJ 8: el efecto corre SOLO cuando cambia unidades (arreglo de dependencias).
  // Con [] correría una sola vez; sin arreglo, en CADA dibujo. En desarrollo,
  // StrictMode lo ejecuta DOS VECES al montar (por eso el console.log se repite).
  useEffect(() => {
    document.title = `Carrito (${unidades}) · Cafetería`
    console.log('Efecto del carrito: unidades =', unidades)
  }, [unidades])

  return (
    <div>
      <h3>Carrito</h3>
      {lineas.length === 0 && <p>El carrito está vacío</p>}
      <ul>
        {lineas.map((l) => (
          <li key={l.id}>
            {l.nombre} x {l.cantidad} — S/ {(Number(l.precio) * l.cantidad).toFixed(2)}{' '}
            <button onClick={() => onQuitar(l.id)}>Quitar</button>
          </li>
        ))}
      </ul>
      <p>Unidades: {unidades}</p>
      <p>Total: S/ {total.toFixed(2)}</p>
      <button onClick={onVaciar}>Vaciar carrito</button>
    </div>
  )
}

export default Carrito
