// Una fila del listado: muestra al prestador y avisa al padre con las funciones recibidas
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
