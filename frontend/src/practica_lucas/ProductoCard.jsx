function ProductoCard({ producto, onAgregar }) {
  return (
    <li className="producto">
      <strong>{producto.nombre}</strong> — S/ {Number(producto.precio).toFixed(2)}{' '}
      {producto.stock === 0 ? (
        <span className="agotado-cafe">Agotado</span>
      ) : (
        <span>Stock: {producto.stock}</span>
      )}{' '}
      <button onClick={() => onAgregar(producto)} disabled={producto.stock === 0}>
        Agregar
      </button>
    </li>
  )
}

export default ProductoCard
