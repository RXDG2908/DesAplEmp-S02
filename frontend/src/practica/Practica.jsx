// ==================================================================
// ARCHIVO  : practica/Practica.jsx
// PARTE 1  : práctica del Lab 11 (mini catálogo con carrito: CAFETERÍA)
// ROL      : COMPONENTE PADRE -> guarda el ESTADO y lo reparte a los hijos.
// ------------------------------------------------------------------
// LAB 11 - EJ 1: PASA los productos a Catalogo POR PROPS.
// LAB 11 - EJ 3: agregarAlCarrito se ENLAZA hasta ProductoCard (onAgregar).
// LAB 11 - EJ 4: ESTADO ELEVADO -> el carrito vive AQUÍ, no en Catalogo ni en ProductoCard.
// LAB 11 - EJ 6: quitar con filter() y vaciar con []; NUNCA push ni splice.
// LAB 11 - EJ 7: el texto del Buscador vive aquí y FILTRA antes de llegar a Catalogo.
// LAB 11 - EJ 8: el mensaje de <Aviso> también vive en el padre.
// ------------------------------------------------------------------
// USA      : ./Catalogo.jsx, ./Carrito.jsx, ./Buscador.jsx, ../components/Aviso.jsx
// ==================================================================
import { useState } from 'react'
import { productos } from './datos.js'
import Catalogo from './Catalogo.jsx'
import Carrito from './Carrito.jsx'
import Buscador from './Buscador.jsx'
import Aviso from '../components/Aviso.jsx'

// COMPONENTE PADRE: guarda el CARRITO, el TEXTO DE BÚSQUEDA y el AVISO.
function Practica() {
  const [carrito, setCarrito] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState('')

  // LAB 11 - EJ 7: FILTRO con filter() + includes() sin distinguir mayúsculas.
  const visibles = productos.filter((p) =>
    p.nombre.toLowerCase().includes(busqueda.toLowerCase())
  )

  // LAB 11 - EJ 4: si el producto YA ESTÁ, aumenta su cantidad con map();
  // si NO está, agrega una línea nueva con un ARREGLO NUEVO (spread).
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

  // LAB 11 - EJ 6: QUITAR con filter() y VACIAR con un arreglo vacío.
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
