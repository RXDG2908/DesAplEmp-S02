// Resumen hermano del listado: todo se calcula con las citas recibidas, sin estado propio
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
