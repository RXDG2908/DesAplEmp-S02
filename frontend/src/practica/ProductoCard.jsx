// ==================================================================
// ARCHIVO  : practica/ProductoCard.jsx
// PARTE 1  : práctica del Lab 11 (mini catálogo con carrito: CAFETERÍA)
// ------------------------------------------------------------------
// LAB 11 - EJ 1: muestra nombre, precio con Number(...).toFixed(2) y AGOTADO si stock = 0.
// LAB 11 - EJ 2: la prop producto es de SOLO LECTURA; esta tarjeta NO la modifica.
// LAB 11 - EJ 3: el botón Agregar (DESACTIVADO sin stock) AVISA AL PADRE con onAgregar.
//                Se escribe () => onAgregar(producto); con onAgregar(producto) a secas
//                la función se EJECUTARÍA AL DIBUJAR, no al hacer clic.
// ------------------------------------------------------------------
// USADO EN : ./Catalogo.jsx
// ==================================================================
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
