// ==================================================================
// ARCHIVO  : pages/ProductosPage.jsx
// PARTE 1  : PRÁCTICA: tienda en línea de la CAFETERÍA
// ROL      : PANTALLA del CATÁLOGO: lista los productos que entrega la API de Django.
// ------------------------------------------------------------------
// LAB 13 - EJ 7: archivo creado vacío en la estructura (pages = pantallas completas).
// LAB 14 - EJ 7: GET /api/productos/ con api.get dentro de useEffect; tabla con map() y key.
// ------------------------------------------------------------------
// MAPA DE RUTAS: React /productos  <->  API /api/productos/
// USA      : ../api.js  ·  USADO EN: ../App.jsx (vista 'productos')
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 13 - EJ 7 .... línea 19
//   LAB 14 - EJ 7 .... línea 24
// ==================================================================
import { useEffect, useState } from 'react'
import api from '../api.js'

function ProductosPage() {
  const [productos, setProductos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(false)

  // LAB 14 - EJ 7: la lista se pide UNA VEZ al mostrar la pantalla (arreglo de dependencias vacío).
  useEffect(() => {
    async function cargar() {
      try {
        const respuesta = await api.get('/productos/')
        setProductos(respuesta.data)
      } catch (err) {
        console.log('Error al cargar los productos:', err.message)
        setError(true)
      } finally {
        setCargando(false)
      }
    }
    cargar()
  }, [])

  return (
    <div className="seccion-vet">
      <h2>Cafetería: catálogo desde la API</h2>
      {cargando && <p>Cargando...</p>}
      {error && <p className="error">No se pudo cargar el catálogo</p>}
      {!cargando && !error && (
        <table className="tabla-libros">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Categoría</th>
              <th>Precio</th>
              <th>Stock</th>
            </tr>
          </thead>
          <tbody>
            {productos.map((p) => (
              <tr key={p.id}>
                <td>{p.nombre}</td>
                <td>{p.categoria_nombre}</td>
                <td>S/ {Number(p.precio).toFixed(2)}</td>
                <td>{p.stock === 0 ? <span className="agotado">Agotado</span> : p.stock}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default ProductosPage
