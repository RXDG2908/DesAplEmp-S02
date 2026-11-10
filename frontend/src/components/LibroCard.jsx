import { useState } from 'react'

function LibroCard({ titulo, autor, anio, copias, categoria = 'Sin categoría' }) {
  const [reservas, setReservas] = useState(0)

  return (
    <li>
      {titulo} ({anio}) — {autor} — {categoria} —{' '}
      {copias === 0 ? <span className="agotado">Agotado</span> : `Copias: ${copias}`}
      {copias === 1 && <strong> ¡Última copia!</strong>}{' '}
      <button
        onClick={() => setReservas(reservas + 1)}
        disabled={copias === 0 || reservas >= copias}
      >
        Reservar
      </button>
      {reservas > 0 && <span> Reservados: {reservas}</span>}
    </li>
  )
}

export default LibroCard