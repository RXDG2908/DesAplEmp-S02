// Una fila del listado: muestra al prestador y avisa al padre con las funciones recibidas
function PrestadorFila({ prestador, onAprobar, onSuspender, onEliminar }) {
  return (
    <tr>
      <td>
        {prestador.nombres} {prestador.apellidos}
      </td>
      <td>{prestador.rubro}</td>
      <td>S/ {Number(prestador.tarifa).toFixed(2)}</td>
      <td>{prestador.estado}</td>
      <td>
        <button onClick={() => onAprobar(prestador.id)} disabled={prestador.estado === 'Aprobado'}>
          Aprobar
        </button>{' '}
        <button onClick={() => onSuspender(prestador.id)} disabled={prestador.estado === 'Suspendido'}>
          Suspender
        </button>{' '}
        <button onClick={() => onEliminar(prestador.id)}>Eliminar</button>
      </td>
    </tr>
  )
}

export default PrestadorFila
