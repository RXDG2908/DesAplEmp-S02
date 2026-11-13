import { useEffect, useState } from 'react'
import { citasPanel } from '../datos.js'
import CitaListado from './CitaListado.jsx'
import CitaForm from './CitaForm.jsx'
import ResumenCitas from './ResumenCitas.jsx'
import BuscadorCitas from './BuscadorCitas.jsx'
import Aviso from './Aviso.jsx'

// Componente padre del panel: aquí vive el estado de las citas
function PanelCitas() {
  const [citas, setCitas] = useState(citasPanel)
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState('')

  const visibles = citas.filter((c) =>
    c.mascota.toLowerCase().includes(busqueda.toLowerCase())
  )

  // El título de la pestaña sigue la cantidad de citas
  useEffect(() => {
    document.title = `Panel de citas (${citas.length})`
  }, [citas.length])

  function guardarCita(datos) {
    const nueva = { id: Math.max(0, ...citas.map((c) => c.id)) + 1, ...datos, estado: 'Pendiente' }
    setCitas([...citas, nueva])
    setAviso(`Cita guardada: ${nueva.mascota}`)
  }

  function eliminarCita(id) {
    setCitas(citas.filter((c) => c.id !== id))
  }

  function confirmarCita(id) {
    setCitas(citas.map((c) => (c.id === id ? { ...c, estado: 'Confirmada' } : c)))
  }

  return (
    <div className="seccion-vet">
      <h2>Panel administrativo: citas</h2>
      <CitaForm onGuardar={guardarCita} />
      <Aviso mensaje={aviso} onTerminar={() => setAviso('')} />
      <BuscadorCitas valor={busqueda} onCambiar={setBusqueda} />
      <CitaListado citas={visibles} onConfirmar={confirmarCita} onEliminar={eliminarCita} />
      <ResumenCitas citas={citas} />
    </div>
  )
}

export default PanelCitas
