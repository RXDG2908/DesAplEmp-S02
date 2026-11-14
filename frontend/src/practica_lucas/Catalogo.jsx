import ProductoCard from './ProductoCard.jsx'

function Catalogo({ productos, onAgregar }) {
  if (productos.length === 0) {
    return <p>No hay productos que coincidan</p>
  }

  return (
    <ul>
      {productos.map((producto) => (
        <ProductoCard key={producto.id} producto={producto} onAgregar={onAgregar} />
      ))}
    </ul>
  )
}

export default Catalogo
