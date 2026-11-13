import { useState } from 'react'
import { insumos } from './datos.js'
import Catalogo from './Catalogo.jsx'
import Consumo from './Consumo.jsx'
import Buscador from './Buscador.jsx'
import Aviso from '../components/Aviso.jsx'

// Componente padre: guarda el consumo, el texto de búsqueda y el aviso
function Practica() {
  const [consumo, setConsumo] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState('')

  const visibles = insumos.filter((i) =>
    i.nombre.toLowerCase().includes(busqueda.toLowerCase())
  )

  function agregarAlConsumo(insumo) {
    const existe = consumo.some((l) => l.id === insumo.id)
    if (existe) {
      setConsumo(
        consumo.map((l) => (l.id === insumo.id ? { ...l, cantidad: l.cantidad + 1 } : l))
      )
    } else {
      setConsumo([
        ...consumo,
        { id: insumo.id, nombre: insumo.nombre, precio: insumo.precio, cantidad: 1 },
      ])
    }
    setAviso(`Agregado: ${insumo.nombre}`)
  }

  function quitarDelConsumo(id) {
    setConsumo(consumo.filter((l) => l.id !== id))
  }

  function vaciarConsumo() {
    setConsumo([])
  }

  return (
    <div className="seccion-vet">
      <h2>Veterinaria: comunicación entre componentes</h2>
      <Buscador valor={busqueda} onCambiar={setBusqueda} />
      <Catalogo insumos={visibles} onAgregar={agregarAlConsumo} />
      <Consumo lineas={consumo} onQuitar={quitarDelConsumo} onVaciar={vaciarConsumo} />
      <Aviso mensaje={aviso} onTerminar={() => setAviso('')} />
    </div>
  )
}

export default Practica
