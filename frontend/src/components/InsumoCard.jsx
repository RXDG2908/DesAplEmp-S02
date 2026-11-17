// ==================================================================
// ARCHIVO  : components/InsumoCard.jsx
// PARTE 1  : VET (reserva de citas de la veterinaria)
// ROL      : UN INSUMO con su botón Reservar.
// ------------------------------------------------------------------
// LAB 10 - EJ 2: PRIMER COMPONENTE FUNCIONAL (nombre en MAYÚSCULA + export default).
// LAB 10 - EJ 3: PROPS DESESTRUCTURADAS (nombre, unidad, stock); unidad tiene VALOR POR DEFECTO.
// LAB 10 - EJ 6: ESTADO LOCAL con useState + evento onClick (contador de reservados).
// LAB 9 - EJ 6 : RENDERIZADO CONDICIONAL -> ternario (Sin stock / Stock: n) y &&.
// ------------------------------------------------------------------
// USADO EN : ./InsumoLista.jsx
// ==================================================================
import { useState } from 'react'

// LAB 10 - EJ 6: cada tarjeta lleva SU PROPIO CONTADOR (estado local, no compartido).
function InsumoCard({ nombre, unidad = 'unidad', stock }) {
  const [reservados, setReservados] = useState(0)
  // El botón se DESACTIVA si no hay stock o si ya se reservó todo.
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
