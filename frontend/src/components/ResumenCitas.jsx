// ==================================================================
// ARCHIVO  : components/ResumenCitas.jsx
// PARTE 1  : VET (panel de citas, primera versión del Lab 11)
// ROL      : RESUMEN de las citas por estado (datos derivados, sin useState).
// ------------------------------------------------------------------
// LAB 11 - EJ 13: RESUMEN HERMANO del listado; el CONTEO POR ESTADO se calcula
//                 con las citas recibidas, SIN useState (DATOS DERIVADOS).
// ------------------------------------------------------------------
// USADO EN : ./PanelCitas.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 13 ... línea 15
// ==================================================================
function ResumenCitas({ citas }) {
  const pendientes = citas.filter((c) => c.estado === 'Pendiente').length
  const confirmadas = citas.filter((c) => c.estado === 'Confirmada').length
  const atendidas = citas.filter((c) => c.estado === 'Atendida').length

  return (
    <div className="panel-resumen">
      <h3>Resumen</h3>
      <p>Citas registradas: {citas.length}</p>
      <p>Pendientes: {pendientes}</p>
      <p>Confirmadas: {confirmadas}</p>
      <p>Atendidas: {atendidas}</p>
    </div>
  )
}

export default ResumenCitas
