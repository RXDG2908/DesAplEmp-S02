import CitaFila from './CitaFila.jsx'

// Tabla de citas: recibe la lista por props y entrega cada cita a su fila
function CitaListado({ citas, onConfirmar, onEliminar }) {
  if (citas.length === 0) {
    return <p>No hay citas que coincidan</p>
  }

  return (
    <table className="tabla-libros">
      <thead>
        <tr>
          <th>Mascota</th>
          <th>Dueño</th>
          <th>Servicio</th>
          <th>Hora</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {citas.map((cita) => (
          <CitaFila key={cita.id} cita={cita} onConfirmar={onConfirmar} onEliminar={onEliminar} />
        ))}
      </tbody>
    </table>
  )
}

export default CitaListado
