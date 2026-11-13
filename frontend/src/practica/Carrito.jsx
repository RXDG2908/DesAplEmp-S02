import { useEffect } from 'react'

// Muestra las líneas del carrito y avisa al padre al quitar o vaciar
function Carrito({ lineas, onQuitar, onVaciar }) {
  // Datos derivados: se calculan en cada dibujo, no necesitan su propio estado
  const total = lineas.reduce((suma, l) => suma + Number(l.precio) * l.cantidad, 0)
  const unidades = lineas.reduce((suma, l) => suma + l.cantidad, 0)

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
