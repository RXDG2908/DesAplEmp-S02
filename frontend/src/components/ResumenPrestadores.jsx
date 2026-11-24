// ==================================================================
// ARCHIVO  : components/ResumenPrestadores.jsx
// PROYECTO : CHAMBA PE (proyecto integrador)
// ROL      : RESUMEN de prestadores: total, conteo por estado y tarifa promedio.
// ------------------------------------------------------------------
// LAB 11 - EJ 13: RESUMEN HERMANO del listado -> TOTAL, CONTEO POR ESTADO y
//                 TARIFA PROMEDIO, calculados SIN useState (DATOS DERIVADOS).
// LAB 12 - EJ 13: ahora se calcula con los datos RECIBIDOS DE LA API.
// ------------------------------------------------------------------
// USADO EN : ./PanelPrestadores.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 13 ... línea 17
//   LAB 12 - EJ 13 ... línea 23
// ==================================================================
function ResumenPrestadores({ prestadores }) {
  const aprobados = prestadores.filter((p) => p.estado === 'Aprobado').length
  const pendientes = prestadores.filter((p) => p.estado === 'Pendiente').length
  const suspendidos = prestadores.filter((p) => p.estado === 'Suspendido').length
  const promedio =
    prestadores.length === 0
      ? 0
      : prestadores.reduce((suma, p) => suma + Number(p.tarifa), 0) / prestadores.length

  return (
    <div className="panel-resumen">
      <h3>Resumen</h3>
      <p>Prestadores registrados: {prestadores.length}</p>
      <p>Aprobados: {aprobados} · Pendientes: {pendientes} · Suspendidos: {suspendidos}</p>
      <p>Tarifa promedio: S/ {promedio.toFixed(2)}</p>
    </div>
  )
}

export default ResumenPrestadores
