import { useEffect } from 'react'

function Carrito({ lineas, onQuitar, onVaciar }) {
  const total = lineas.reduce((suma, l) => suma + Number(l.precio) * l.cantidad, 0)
  const unidades = lineas.reduce((suma, l) => suma + l.cantidad, 0)

  useEffect(() => {
    console.log('Efecto ejecutado. Unidades:', unidades)
    document.title = `Carrito (${unidades}) — Cafetería`
  }, [unidades])

  return (
    <div className="carrito">
      <h2>Carrito</h2>
      {lineas.length === 0 && <p>El carrito está vacío</p>}
      <ul>
        {lineas.map((linea) => (
          <li key={linea.id}>
            {linea.nombre} x {linea.cantidad} — S/{' '}
            {(Number(linea.precio) * linea.cantidad).toFixed(2)}{' '}
            <button onClick={() => onQuitar(linea.id)}>Quitar</button>
          </li>
        ))}
      </ul>
      <p>Unidades: {unidades}</p>
      <p>Total: S/ {total.toFixed(2)}</p>
      <button onClick={onVaciar} disabled={lineas.length === 0}>
        Vaciar carrito
      </button>
    </div>
  )
}

export default Carrito
