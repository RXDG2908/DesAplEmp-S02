import { useState } from 'react'
import { productos } from './datos.js'
import Catalogo from './Catalogo.jsx'
import Carrito from './Carrito.jsx'
import Buscador from './Buscador.jsx'
import Aviso from '../components/Aviso.jsx'

// Componente padre: guarda el carrito, el texto de búsqueda y el aviso
function Practica() {
  const [carrito, setCarrito] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState('')

  const visibles = productos.filter((p) =>
    p.nombre.toLowerCase().includes(busqueda.toLowerCase())
  )

  function agregarAlCarrito(producto) {
    const existe = carrito.some((l) => l.id === producto.id)
    if (existe) {
      setCarrito(
        carrito.map((l) => (l.id === producto.id ? { ...l, cantidad: l.cantidad + 1 } : l))
      )
    } else {
      setCarrito([
        ...carrito,
        { id: producto.id, nombre: producto.nombre, precio: producto.precio, cantidad: 1 },
      ])
    }
    setAviso(`Agregado: ${producto.nombre}`)
  }

  function quitarDelCarrito(id) {
    setCarrito(carrito.filter((l) => l.id !== id))
  }

  function vaciarCarrito() {
    setCarrito([])
  }

  return (
    <div className="seccion-vet">
      <h2>Cafetería: comunicación entre componentes</h2>
      <Buscador valor={busqueda} onCambiar={setBusqueda} />
      <Catalogo productos={visibles} onAgregar={agregarAlCarrito} />
      <Carrito lineas={carrito} onQuitar={quitarDelCarrito} onVaciar={vaciarCarrito} />
      <Aviso mensaje={aviso} onTerminar={setAviso} />
    </div>
  )
}

export default Practica
