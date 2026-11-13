// Una fila del listado: muestra la cita y avisa al padre con las funciones recibidas
function CitaFila({ cita, onConfirmar, onEliminar }) {
  return (
    <tr>
      <td>{cita.mascota}</td>
      <td>{cita.dueno}</td>
      <td>{cita.servicio}</td>
      <td>{cita.hora}</td>
      <td>{cita.estado}</td>
      <td>
        <button onClick={() => onConfirmar(cita.id)} disabled={cita.estado !== 'Pendiente'}>
          Confirmar
        </button>{' '}
        <button onClick={() => onEliminar(cita.id)}>Eliminar</button>
      </td>
    </tr>
  )
}

export default CitaFila
