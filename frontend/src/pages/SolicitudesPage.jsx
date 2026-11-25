// ==================================================================
// ARCHIVO  : pages/SolicitudesPage.jsx
// PROYECTO : CHAMBA PE (proyecto integrador)
// ROL      : PANTALLA DE LISTADO de las solicitudes de servicio (operación principal).
// ------------------------------------------------------------------
// LAB 13 - EJ 13: archivo creado vacío en la estructura.
// LAB 14 - EJ 12: GET /api/solicitudes/ con estados CARGANDO y ERROR, búsqueda (?search=)
//                 y filtro por estado (?estado=). Al pulsar "Ver" se abre el DETALLE:
//                 la navegación usa ESTADO LOCAL (seleccionada) en lugar de un router.
// ------------------------------------------------------------------
// MAPA DE RUTAS: React /solicitudes  <->  API /api/solicitudes/
// USA      : ../api.js, ./SolicitudDetallePage.jsx  ·  USADO EN: ../App.jsx (vista 'solicitudes')
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 13 - EJ 13 ... línea 22
//   LAB 14 - EJ 12 ... línea 31
// ==================================================================
import { useEffect, useState } from 'react'
import api from '../api.js'
import SolicitudDetallePage from './SolicitudDetallePage.jsx'

function SolicitudesPage() {
  const [solicitudes, setSolicitudes] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(false)
  const [buscar, setBuscar] = useState('')
  const [estado, setEstado] = useState('')
  // id de la solicitud abierta; null = se ve el listado (equivale a la ruta /solicitudes/:id)
  const [seleccionada, setSeleccionada] = useState(null)

  // LAB 14 - EJ 12: la lista se vuelve a pedir cuando cambian la búsqueda, el filtro
  // o cuando se vuelve del detalle (por si allí cambió el estado).
  useEffect(() => {
    if (seleccionada !== null) return
    async function cargar() {
      try {
        const respuesta = await api.get('/solicitudes/', { params: { search: buscar, estado: estado } })
        setSolicitudes(respuesta.data)
        setError(false)
      } catch (err) {
        console.log('Error al cargar las solicitudes:', err.message)
        setError(true)
      } finally {
        setCargando(false)
      }
    }
    cargar()
  }, [buscar, estado, seleccionada])

  if (seleccionada !== null) {
    return <SolicitudDetallePage id={seleccionada} onVolver={() => setSeleccionada(null)} />
  }

  return (
    <div className="seccion-vet">
      <h2>Chamba PE — Solicitudes de servicio</h2>
      <input
        type="text"
        placeholder="Buscar por cliente, prestador o rubro"
        value={buscar}
        onChange={(e) => setBuscar(e.target.value)}
      />
      <select value={estado} onChange={(e) => setEstado(e.target.value)}>
        <option value="">Todos los estados</option>
        <option value="PEN">Pendiente</option>
        <option value="CON">Confirmada</option>
        <option value="CAM">En camino</option>
        <option value="SER">En servicio</option>
        <option value="FIN">Finalizada</option>
        <option value="PAG">Pagada</option>
      </select>
      {cargando && <p>Cargando...</p>}
      {error && <p className="error">No se pudo cargar la lista de solicitudes</p>}
      {!cargando && !error && solicitudes.length === 0 && <p>No hay solicitudes que coincidan</p>}
      {!cargando && !error && solicitudes.length > 0 && (
        <table className="tabla-libros">
          <thead>
            <tr>
              <th>N.°</th>
              <th>Cliente</th>
              <th>Prestador</th>
              <th>Rubro</th>
              <th>Estado</th>
              <th>Monto</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {solicitudes.map((s) => (
              <tr key={s.id}>
                <td>{s.id}</td>
                <td>{s.cliente_nombre}</td>
                <td>{s.prestador_nombre}</td>
                <td>{s.rubro_nombre}</td>
                <td>{s.estado_nombre}</td>
                <td>S/ {Number(s.monto).toFixed(2)}</td>
                <td>
                  <button onClick={() => setSeleccionada(s.id)}>Ver</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default SolicitudesPage
