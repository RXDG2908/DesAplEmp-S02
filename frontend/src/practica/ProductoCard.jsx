// Muestra un producto y avisa al padre cuando se pulsa Agregar
function ProductoCard({ producto, onAgregar }) {
  return (
    <li>
      {producto.nombre} — S/ {Number(producto.precio).toFixed(2)} —{' '}
      {producto.stock === 0 ? (
        <span className="agotado">Agotado</span>
      ) : (
        `Stock: ${producto.stock}`
      )}{' '}
      <button onClick={() => onAgregar(producto)} disabled={producto.stock === 0}>
        Agregar
      </button>
    </li>
  )
}

export default ProductoCard
