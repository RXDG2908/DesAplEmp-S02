// ==================================================================
// ARCHIVO  : pages/SolicitudDetallePage.jsx
// PROYECTO : CHAMBA PE (proyecto integrador)
// ROL      : PANTALLA DE DETALLE de una solicitud: datos, monto y SEGUIMIENTO de estados.
// ------------------------------------------------------------------
// LAB 14 - EJ 12: GET /api/solicitudes/<id>/ (equivale a la ruta de React /solicitudes/:id)
//                 con CARGANDO y ERROR. El botón "Avanzar estado" llama a
//                 POST /api/solicitudes/<id>/avanzar/; el orden lo controla Django.
// ------------------------------------------------------------------
// USA      : ../api.js  ·  USADO EN: ./SolicitudesPage.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 14 - EJ 12 ... línea 22
// ==================================================================
import { useEffect, useState } from 'react'
import api, { textoError } from '../api.js'

function SolicitudDetallePage({ id, onVolver }) {
  const [solicitud, setSolicitud] = useState(null)
  const [error, setError] = useState('')

  // LAB 14 - EJ 12: se pide el registro cada vez que cambia el id.
  useEffect(() => {
    async function cargar() {
      try {
        const respuesta = await api.get(`/solicitudes/${id}/`)
        setSolicitud(respuesta.data)
        setError('')
      } catch (err) {
        setError(textoError(err))
      }
    }
    cargar()
  }, [id])

  async function avanzar() {
    try {
      const respuesta = await api.post(`/solicitudes/${id}/avanzar/`)
      setSolicitud(respuesta.data)
      setError('')
    } catch (err) {
      setError(textoError(err))
    }
  }

  return (
    <div className="seccion-vet">
      <button onClick={onVolver}>← Volver al listado</button>
      {!solicitud && !error && <p>Cargando...</p>}
      {error && <p className="error">{error}</p>}
      {solicitud && (
        <div className="panel-resumen">
          <h2>Solicitud N.° {solicitud.id}</h2>
          <p>Cliente: {solicitud.cliente_nombre}</p>
          <p>
            Prestador: {solicitud.prestador_nombre} ({solicitud.rubro_nombre})
          </p>
          <p>Dirección: {solicitud.direccion}</p>
          <p>Detalle: {solicitud.descripcion || '—'}</p>
          <p>Monto: S/ {Number(solicitud.monto).toFixed(2)}</p>
          <p>
            Estado actual: <strong>{solicitud.estado_nombre}</strong>{' '}
            <button onClick={avanzar}>Avanzar estado</button>
          </p>
          <h3>Seguimiento</h3>
          <ul>
            {solicitud.seguimiento.map((paso, i) => (
              <li key={i}>
                {new Date(paso.fecha).toLocaleString('es-PE')} — {paso.estado_nombre}
                {paso.nota && ` (${paso.nota})`}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default SolicitudDetallePage
