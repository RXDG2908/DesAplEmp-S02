import { useState } from 'react'
import { productos } from './datos.js'
import Buscador from './Buscador.jsx'
import Catalogo from './Catalogo.jsx'
import Carrito from './Carrito.jsx'
import Aviso from './Aviso.jsx'
import './practica_lucas.css'

function PracticaLucas() {
  const [carrito, setCarrito] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState(null)

  function agregarAlCarrito(producto) {
    console.log('Agregar:', producto.nombre)
    const existe = carrito.some((linea) => linea.id === producto.id)
    if (existe) {
      setCarrito(
        carrito.map((linea) =>
          linea.id === producto.id ? { ...linea, cantidad: linea.cantidad + 1 } : linea
        )
      )
    } else {
      setCarrito([
        ...carrito,
        { id: producto.id, nombre: producto.nombre, precio: producto.precio, cantidad: 1 },
      ])
    }
    setAviso({ id: Date.now(), nombre: producto.nombre })
  }

  function quitarDelCarrito(id) {
    setCarrito(carrito.filter((linea) => linea.id !== id))
  }

  function vaciarCarrito() {
    setCarrito([])
  }

  const filtrados = productos.filter((producto) =>
    producto.nombre.toLowerCase().includes(busqueda.toLowerCase())
  )

  return (
    <div className="practica-lucas">
      <h1>Cafetería</h1>
      {aviso && <Aviso key={aviso.id} nombre={aviso.nombre} />}
      <Buscador valor={busqueda} onCambiar={setBusqueda} />
      <div className="columnas">
        <div>
          <h2>Catálogo</h2>
          <Catalogo productos={filtrados} onAgregar={agregarAlCarrito} />
        </div>
        <Carrito lineas={carrito} onQuitar={quitarDelCarrito} onVaciar={vaciarCarrito} />
      </div>
    </div>
  )
}

export default PracticaLucas
