// ==================================================================
// ARCHIVO  : components/PanelCitas.jsx
// PARTE 1  : VET (reserva de citas de la veterinaria)
// ROL      : COMPONENTE PADRE del panel administrativo de CITAS.
// NOTA     : PRIMERA VERSIÓN del panel del Lab 11 (con la veterinaria); la
//            entrega final del panel se hizo con CHAMBA PE (PanelPrestadores).
// ------------------------------------------------------------------
// LAB 11 - EJ 10: ESTADO ELEVADO -> las citas viven AQUÍ (useState) y bajan por props.
// LAB 11 - EJ 11: confirmar con map() y eliminar con filter(); NUNCA push ni splice.
// LAB 11 - EJ 12: guardarCita recibe la cita nueva del FORMULARIO HIJO (onGuardar).
// LAB 11 - EJ 13: BUSCADOR, RESUMEN hermano y useEffect con el título de la pestaña.
// ------------------------------------------------------------------
// USA      : ./CitaForm, ./Aviso, ./BuscadorCitas, ./CitaListado, ./ResumenCitas
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 10 ... línea 31
//   LAB 11 - EJ 11 ... línea 52
//   LAB 11 - EJ 12 ... línea 45
//   LAB 11 - EJ 13 ... líneas 35, 40
// ==================================================================
import { useEffect, useState } from 'react'
import { citasPanel } from '../datos.js'
import CitaListado from './CitaListado.jsx'
import CitaForm from './CitaForm.jsx'
import ResumenCitas from './ResumenCitas.jsx'
import BuscadorCitas from './BuscadorCitas.jsx'
import Aviso from './Aviso.jsx'

// COMPONENTE PADRE: aquí vive el ESTADO de las citas, la búsqueda y el aviso.
function PanelCitas() {
  const [citas, setCitas] = useState(citasPanel)
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState('')

  // LAB 11 - EJ 13: FILTRO por mascota antes de entregar la lista al listado.
  const visibles = citas.filter((c) =>
    c.mascota.toLowerCase().includes(busqueda.toLowerCase())
  )

  // LAB 11 - EJ 13: useEffect -> el TÍTULO DE LA PESTAÑA sigue la cantidad de citas.
  useEffect(() => {
    document.title = `Panel de citas (${citas.length})`
  }, [citas.length])

  // LAB 11 - EJ 12: agrega la cita nueva con un ARREGLO NUEVO (estado inicial 'Pendiente').
  function guardarCita(datos) {
    const nueva = { id: Math.max(0, ...citas.map((c) => c.id)) + 1, ...datos, estado: 'Pendiente' }
    setCitas([...citas, nueva])
    setAviso(`Cita guardada: ${nueva.mascota}`)
  }

  // LAB 11 - EJ 11: ELIMINAR con filter() y CONFIRMAR con map().
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
      <Aviso mensaje={aviso} onTerminar={setAviso} />
      <BuscadorCitas valor={busqueda} onCambiar={setBusqueda} />
      <CitaListado citas={visibles} onConfirmar={confirmarCita} onEliminar={eliminarCita} />
      <ResumenCitas citas={citas} />
    </div>
  )
}

export default PanelCitas
