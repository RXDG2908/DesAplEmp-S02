// Muestra un insumo y avisa al padre cuando se pulsa Agregar
function InsumoCard({ insumo, onAgregar }) {
  return (
    <li>
      {insumo.nombre} — S/ {Number(insumo.precio).toFixed(2)} —{' '}
      {insumo.stock === 0 ? (
        <span className="sin-stock">Agotado</span>
      ) : (
        `Stock: ${insumo.stock}`
      )}{' '}
      <button onClick={() => onAgregar(insumo)} disabled={insumo.stock === 0}>
        Agregar
      </button>
    </li>
  )
}

export default InsumoCard
