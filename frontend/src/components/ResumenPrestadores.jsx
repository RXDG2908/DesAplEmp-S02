// Resumen hermano del listado: todo se calcula con los prestadores recibidos, sin estado propio
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
