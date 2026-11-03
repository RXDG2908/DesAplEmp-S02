import { useState } from 'react'

// Un insumo con un boton de estado local: cada tarjeta lleva su propio contador.
// "unidad" tiene valor por defecto.
function InsumoCard({ nombre, unidad = 'unidad', stock }) {
  const [reservados, setReservados] = useState(0)
  const agotado = stock === 0 || reservados >= stock

  return (
    <li>
      {nombre} ({unidad}) —{' '}
      {stock === 0 ? <span className="sin-stock">Sin stock</span> : `Stock: ${stock}`}{' '}
      <button onClick={() => setReservados(reservados + 1)} disabled={agotado}>
        Reservar
      </button>
      {reservados > 0 && <strong> Reservados: {reservados}</strong>}
    </li>
  )
}

export default InsumoCard
