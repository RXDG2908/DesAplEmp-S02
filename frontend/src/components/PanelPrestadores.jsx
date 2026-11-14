import { useEffect, useState } from 'react'
import api, { textoError } from '../api.js'
import PrestadorListado from './PrestadorListado.jsx'
import PrestadorForm from './PrestadorForm.jsx'
import ResumenPrestadores from './ResumenPrestadores.jsx'
import BuscadorPrestadores from './BuscadorPrestadores.jsx'
import FiltroEstadoPrestador from './FiltroEstadoPrestador.jsx'
import Aviso from './Aviso.jsx'

// Función adaptadora: la API entrega la tarifa como texto ("60.00") y el panel la usa como número
function adaptar(prestador) {
  return { ...prestador, tarifa: Number(prestador.tarifa) }
}

// Componente padre del panel de Chamba PE: guarda los prestadores y los estados de la petición
function PanelPrestadores() {
  const [prestadores, setPrestadores] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(false)
  const [busqueda, setBusqueda] = useState('')
  const [estado, setEstado] = useState('')
  const [editando, setEditando] = useState(null)
  const [porEliminar, setPorEliminar] = useState(null)
  const [aviso, setAviso] = useState('')

  // Se vuelve a pedir la lista cuando cambian la búsqueda o el filtro
  useEffect(() => {
    const controlador = new AbortController()
    async function cargar() {
      try {
        const respuesta = await api.get('/chamba/prestadores/', {
          params: { search: busqueda, estado: estado },
          signal: controlador.signal,
        })
        setPrestadores(respuesta.data.map(adaptar))
        setError(false)
      } catch (err) {
        if (err.name === 'CanceledError') return
        console.log('Error al cargar los prestadores:', err.message)
        setError(true)
      }
      setCargando(false)
    }
    cargar()
    // Limpieza: cancela la petición pendiente si cambian los parámetros
    return () => controlador.abort()
  }, [busqueda, estado])

  // El título de la pestaña sigue la cantidad de prestadores
  useEffect(() => {
    document.title = `Panel Chamba PE (${prestadores.length})`
  }, [prestadores.length])

  // Devuelve el texto del error de la API, o vacío si todo salió bien
  async function guardarPrestador(datos) {
    try {
      if (editando) {
        const respuesta = await api.patch(`/chamba/prestadores/${editando.id}/`, datos)
        setPrestadores(prestadores.map((p) => (p.id === editando.id ? adaptar(respuesta.data) : p)))
        setAviso(`Prestador actualizado: ${datos.nombres}`)
        setEditando(null)
      } else {
        const respuesta = await api.post('/chamba/prestadores/', datos)
        setPrestadores([...prestadores, adaptar(respuesta.data)])
        setAviso(`Prestador registrado: ${datos.nombres}`)
      }
      return ''
    } catch (err) {
      return textoError(err)
    }
  }

  async function cambiarEstado(prestador, nuevoEstado) {
    try {
      const respuesta = await api.patch(`/chamba/prestadores/${prestador.id}/`, { estado: nuevoEstado })
      setPrestadores(prestadores.map((p) => (p.id === prestador.id ? adaptar(respuesta.data) : p)))
    } catch (err) {
      setAviso(textoError(err))
    }
  }

  // Primer clic en Eliminar: pide confirmar. Segundo clic (Confirmar): borra en la API
  async function eliminarPrestador(id) {
    if (porEliminar !== id) {
      setPorEliminar(id)
      return
    }
    setPorEliminar(null)
    try {
      await api.delete(`/chamba/prestadores/${id}/`)
      setPrestadores(prestadores.filter((p) => p.id !== id))
      setAviso('Prestador eliminado')
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setPrestadores(prestadores.filter((p) => p.id !== id))
        setAviso('El prestador ya no existe en el servidor')
      } else {
        setAviso(textoError(err))
      }
    }
  }

  return (
    <div className="seccion-vet">
      <h2>Chamba PE — Panel administrativo: prestadores</h2>
      <PrestadorForm
        key={editando ? editando.id : 'nuevo'}
        prestador={editando}
        onGuardar={guardarPrestador}
        onCancelar={() => setEditando(null)}
      />
      <Aviso mensaje={aviso} onTerminar={setAviso} />
      <BuscadorPrestadores valor={busqueda} onCambiar={setBusqueda} />
      <FiltroEstadoPrestador valor={estado} onCambiar={setEstado} />
      {cargando && <p>Cargando...</p>}
      {error && <p className="error">No se pudo cargar la lista de prestadores</p>}
      {!cargando && !error && (
        <PrestadorListado
          prestadores={prestadores}
          porEliminar={porEliminar}
          onEditar={setEditando}
          onCambiarEstado={cambiarEstado}
          onEliminar={eliminarPrestador}
        />
      )}
      <ResumenPrestadores prestadores={prestadores} />
    </div>
  )
}

export default PanelPrestadores
