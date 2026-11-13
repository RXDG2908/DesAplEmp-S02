import { useEffect, useState } from 'react'
import { prestadoresPanel } from '../datosChamba.js'
import PrestadorListado from './PrestadorListado.jsx'
import PrestadorForm from './PrestadorForm.jsx'
import ResumenPrestadores from './ResumenPrestadores.jsx'
import BuscadorPrestadores from './BuscadorPrestadores.jsx'
import Aviso from './Aviso.jsx'

// Componente padre del panel de Chamba PE: aquí vive el estado de los prestadores
function PanelPrestadores() {
  const [prestadores, setPrestadores] = useState(prestadoresPanel)
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState('')

  const visibles = prestadores.filter((p) =>
    `${p.nombres} ${p.apellidos}`.toLowerCase().includes(busqueda.toLowerCase())
  )

  // El título de la pestaña sigue la cantidad de prestadores
  useEffect(() => {
    document.title = `Panel Chamba PE (${prestadores.length})`
  }, [prestadores.length])

  function guardarPrestador(datos) {
    const nuevo = { id: Math.max(0, ...prestadores.map((p) => p.id)) + 1, ...datos, estado: 'Pendiente' }
    setPrestadores([...prestadores, nuevo])
    setAviso(`Prestador registrado: ${nuevo.nombres}`)
  }

  function aprobarPrestador(id) {
    setPrestadores(prestadores.map((p) => (p.id === id ? { ...p, estado: 'Aprobado' } : p)))
  }

  function suspenderPrestador(id) {
    setPrestadores(prestadores.map((p) => (p.id === id ? { ...p, estado: 'Suspendido' } : p)))
  }

  function eliminarPrestador(id) {
    setPrestadores(prestadores.filter((p) => p.id !== id))
  }

  return (
    <div className="seccion-vet">
      <h2>Chamba PE — Panel administrativo: prestadores</h2>
      <PrestadorForm onGuardar={guardarPrestador} />
      <Aviso mensaje={aviso} onTerminar={setAviso} />
      <BuscadorPrestadores valor={busqueda} onCambiar={setBusqueda} />
      <PrestadorListado
        prestadores={visibles}
        onAprobar={aprobarPrestador}
        onSuspender={suspenderPrestador}
        onEliminar={eliminarPrestador}
      />
      <ResumenPrestadores prestadores={prestadores} />
    </div>
  )
}

export default PanelPrestadores
