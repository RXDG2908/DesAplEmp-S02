import PrestadorFila from './PrestadorFila.jsx'

// Tabla de prestadores: recibe la lista por props y entrega cada prestador a su fila
function PrestadorListado({ prestadores, porEliminar, onEditar, onCambiarEstado, onEliminar }) {
  if (prestadores.length === 0) {
    return <p>No hay prestadores que coincidan</p>
  }

  return (
    <table className="tabla-libros">
      <thead>
        <tr>
          <th>Prestador</th>
          <th>Rubro</th>
          <th>Tarifa</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {prestadores.map((prestador) => (
          <PrestadorFila
            key={prestador.id}
            prestador={prestador}
            confirmando={porEliminar === prestador.id}
            onEditar={onEditar}
            onCambiarEstado={onCambiarEstado}
            onEliminar={onEliminar}
          />
        ))}
      </tbody>
    </table>
  )
}

export default PrestadorListado
