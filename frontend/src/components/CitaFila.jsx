// ==================================================================
// ARCHIVO  : components/CitaFila.jsx
// PARTE 1  : VET (panel de citas, primera versión del Lab 11)
// ROL      : UNA FILA de la tabla de citas con sus botones de acción.
// ------------------------------------------------------------------
// LAB 11 - EJ 10: UNA FILA del listado con los datos de la cita.
// LAB 11 - EJ 11: botones Confirmar y Eliminar que AVISAN AL PADRE con las
//                 funciones recibidas; la fila NO MODIFICA la lista por sí misma.
// ------------------------------------------------------------------
// USADO EN : ./CitaListado.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 10 ... línea 18
//   LAB 11 - EJ 11 ... línea 25
// ==================================================================
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
