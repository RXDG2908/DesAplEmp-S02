// ==================================================================
// ARCHIVO  : components/PrestadorFila.jsx
// PROYECTO : CHAMBA PE (proyecto integrador)
// ROL      : UNA FILA de la tabla de prestadores con sus botones de acción.
// ------------------------------------------------------------------
// LAB 11 - EJ 10: UNA FILA con nombre, rubro, tarifa y estado del prestador.
// LAB 11 - EJ 11: botones Aprobar, Suspender y Eliminar que AVISAN AL PADRE;
//                 la fila NO MODIFICA la lista por sí misma.
// LAB 12 - EJ 11: botón Editar -> el padre llena el formulario con este registro.
// LAB 12 - EJ 12: el botón cambia a 'Confirmar' antes de eliminar.
// ------------------------------------------------------------------
// USADO EN : ./PrestadorListado.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 10 ... línea 22
//   LAB 11 - EJ 11 ... línea 32
//   LAB 12 - EJ 11 ... línea 30
//   LAB 12 - EJ 12 ... línea 43
// ==================================================================
function PrestadorFila({ prestador, confirmando, onEditar, onCambiarEstado, onEliminar }) {
  return (
    <tr>
      <td>
        {prestador.nombres} {prestador.apellidos}
      </td>
      <td>{prestador.rubro}</td>
      <td>S/ {prestador.tarifa.toFixed(2)}</td>
      <td>{prestador.estado}</td>
      <td>
        <button onClick={() => onEditar(prestador)}>Editar</button>{' '}
        <button
          onClick={() => onCambiarEstado(prestador, 'Aprobado')}
          disabled={prestador.estado === 'Aprobado'}
        >
          Aprobar
        </button>{' '}
        <button
          onClick={() => onCambiarEstado(prestador, 'Suspendido')}
          disabled={prestador.estado === 'Suspendido'}
        >
          Suspender
        </button>{' '}
        <button onClick={() => onEliminar(prestador.id)}>{confirmando ? 'Confirmar' : 'Eliminar'}</button>
      </td>
    </tr>
  )
}

export default PrestadorFila
