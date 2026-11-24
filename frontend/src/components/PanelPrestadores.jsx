// ==================================================================
// ARCHIVO  : components/PanelPrestadores.jsx
// PROYECTO : CHAMBA PE (proyecto integrador)
// ROL      : COMPONENTE PADRE del PANEL ADMINISTRATIVO de prestadores.
// ------------------------------------------------------------------
// LAB 11 - EJ 10: ESTADO ELEVADO -> los prestadores viven AQUÍ y bajan por props.
// LAB 11 - EJ 11: aprobar / suspender con map() y eliminar con filter().
// LAB 11 - EJ 12: guardarPrestador recibe el registro del FORMULARIO HIJO.
// LAB 11 - EJ 13: BUSCADOR, RESUMEN hermano y useEffect (título de la pestaña).
// LAB 12 - EJ 10: la lista se CARGA DE LA API con GET dentro de un useEffect;
//                 estados CARGANDO y ERROR + función ADAPTADORA de la tarifa.
// LAB 12 - EJ 11: ALTA con POST y EDICIÓN con PATCH (estado actualizado con map()).
// LAB 12 - EJ 12: ELIMINAR con CONFIRMACIÓN (segundo clic) + DELETE; maneja el 404.
// LAB 12 - EJ 13: ?search= y ?estado= viajan a la API; AbortController cancela
//                 la petición pendiente.
// ------------------------------------------------------------------
// USA      : ../api.js, ./PrestadorForm, ./Aviso, ./BuscadorPrestadores,
//            ./FiltroEstadoPrestador, ./PrestadorListado, ./ResumenPrestadores
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 10 ... línea 48
//   LAB 11 - EJ 11 ... línea 105
//   LAB 11 - EJ 12 ... línea 87
//   LAB 11 - EJ 13 ... línea 80
//   LAB 12 - EJ 10 ... líneas 39, 57
//   LAB 12 - EJ 11 ... líneas 85, 105
//   LAB 12 - EJ 12 ... línea 115
//   LAB 12 - EJ 13 ... línea 57
// ==================================================================
import { useEffect, useState } from 'react'
import api, { textoError } from '../api.js'
import PrestadorListado from './PrestadorListado.jsx'
import PrestadorForm from './PrestadorForm.jsx'
import ResumenPrestadores from './ResumenPrestadores.jsx'
import BuscadorPrestadores from './BuscadorPrestadores.jsx'
import FiltroEstadoPrestador from './FiltroEstadoPrestador.jsx'
import Aviso from './Aviso.jsx'

// LAB 12 - EJ 10: FUNCIÓN ADAPTADORA -> la API entrega la tarifa como TEXTO ("60.00")
// y el panel la usa como NÚMERO.
function adaptar(prestador) {
  return { ...prestador, tarifa: Number(prestador.tarifa) }
}

// COMPONENTE PADRE: guarda los prestadores, los ESTADOS DE LA PETICIÓN
// (cargando / error), el filtro, el registro EN EDICIÓN y el que espera CONFIRMACIÓN.
function PanelPrestadores() {
  const [prestadores, setPrestadores] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(false)
  const [busqueda, setBusqueda] = useState('')
  const [estado, setEstado] = useState('')
  const [editando, setEditando] = useState(null)
  const [porEliminar, setPorEliminar] = useState(null)
  const [aviso, setAviso] = useState('')

  // LAB 12 - EJ 10 y 13: GET a la API; se VUELVE A PEDIR cuando cambian la búsqueda o el filtro.
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
    // LIMPIEZA: CANCELA la petición pendiente si cambian los parámetros (AbortController).
    return () => controlador.abort()
  }, [busqueda, estado])

  // LAB 11 - EJ 13: el TÍTULO DE LA PESTAÑA sigue la cantidad de prestadores.
  useEffect(() => {
    document.title = `Panel Chamba PE (${prestadores.length})`
  }, [prestadores.length])

  // LAB 12 - EJ 11: PATCH si hay un prestador EN EDICIÓN, POST si es NUEVO.
  // Devuelve el TEXTO DEL ERROR 400 de la API, o '' (vacío) si todo salió bien.
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

  // LAB 11 - EJ 11 / LAB 12 - EJ 11: APROBAR o SUSPENDER con PATCH y map().
  async function cambiarEstado(prestador, nuevoEstado) {
    try {
      const respuesta = await api.patch(`/chamba/prestadores/${prestador.id}/`, { estado: nuevoEstado })
      setPrestadores(prestadores.map((p) => (p.id === prestador.id ? adaptar(respuesta.data) : p)))
    } catch (err) {
      setAviso(textoError(err))
    }
  }

  // LAB 12 - EJ 12: PRIMER CLIC en Eliminar pide CONFIRMAR; SEGUNDO CLIC borra en la API (204).
  // Si el servidor responde 404 (YA NO EXISTE), se quita de la lista y se avisa.
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
