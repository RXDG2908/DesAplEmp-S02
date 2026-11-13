import { useEffect } from 'react'

// Muestra los insumos usados en la cita y avisa al padre al quitar o vaciar
function Consumo({ lineas, onQuitar, onVaciar }) {
  // Datos derivados: se calculan en cada dibujo, no necesitan su propio estado
  const total = lineas.reduce((suma, l) => suma + Number(l.precio) * l.cantidad, 0)
  const unidades = lineas.reduce((suma, l) => suma + l.cantidad, 0)

  useEffect(() => {
    document.title = `Consumo (${unidades}) · Veterinaria`
    console.log('Efecto del consumo: unidades =', unidades)
  }, [unidades])

  return (
    <div>
      <h3>Consumo de la cita</h3>
      {lineas.length === 0 && <p>El consumo está vacío</p>}
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
      <button onClick={onVaciar}>Vaciar consumo</button>
    </div>
  )
}

export default Consumo
