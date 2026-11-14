// Filtro por estado controlado por el padre
function FiltroEstadoPrestador({ valor, onCambiar }) {
  return (
    <select value={valor} onChange={(e) => onCambiar(e.target.value)}>
      <option value="">Todos los estados</option>
      <option>Pendiente</option>
      <option>Aprobado</option>
      <option>Suspendido</option>
    </select>
  )
}

export default FiltroEstadoPrestador
