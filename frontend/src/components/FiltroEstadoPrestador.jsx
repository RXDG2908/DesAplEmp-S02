// ==================================================================
// ARCHIVO  : components/FiltroEstadoPrestador.jsx
// PROYECTO : CHAMBA PE (proyecto integrador)
// ROL      : SELECT para filtrar los prestadores por estado.
// ------------------------------------------------------------------
// LAB 12 - EJ 13: FILTRO POR ESTADO controlado por el padre; viaja a la API
//                 como ?estado= ('' = todos los estados).
// ------------------------------------------------------------------
// USADO EN : ./PanelPrestadores.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 12 - EJ 13 ... línea 16
// ==================================================================
function FiltroEstadoPrestador({ valor, onCambiar }) {
  return (
    <select value={valor} onChange={(e) => onCambiar(e.target.value)}>
      <option value="">Todos los estados</option>
      <option>Pendiente</option>
      <option>Aprobado</option>
      <option>Suspendido</option>
    </select>
  )
}

export default FiltroEstadoPrestador
