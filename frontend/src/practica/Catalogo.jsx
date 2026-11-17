// ==================================================================
// ARCHIVO  : practica/Catalogo.jsx
// PARTE 1  : práctica del Lab 11 (mini catálogo con carrito: CAFETERÍA)
// ------------------------------------------------------------------
// LAB 11 - EJ 1: entrega CADA PRODUCTO a ProductoCard con map() y key = id.
// LAB 11 - EJ 3: solo PASA onAgregar hacia abajo (no lo usa).
// LAB 11 - EJ 7: recibe la lista YA FILTRADA y avisa si no hay resultados.
// ------------------------------------------------------------------
// USADO EN : ./Practica.jsx  ·  USA: ./ProductoCard.jsx
// ==================================================================
import ProductoCard from './ProductoCard.jsx'

// Recibe la lista YA FILTRADA por el padre y entrega cada producto a su tarjeta.
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
