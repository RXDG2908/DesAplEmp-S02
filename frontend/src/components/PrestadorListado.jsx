// ==================================================================
// ARCHIVO  : components/PrestadorListado.jsx
// PROYECTO : CHAMBA PE (proyecto integrador)
// ------------------------------------------------------------------
// LAB 11 - EJ 10: TABLA de prestadores; una PrestadorFila por registro con
//                 map() y key = id.
// LAB 11 - EJ 13: MENSAJE cuando la búsqueda o el filtro no dan resultados.
// LAB 12 - EJ 12: marca la fila que espera CONFIRMACIÓN (porEliminar).
// ------------------------------------------------------------------
// USADO EN : ./PanelPrestadores.jsx  ·  USA: ./PrestadorFila.jsx
// ==================================================================
import PrestadorFila from './PrestadorFila.jsx'

// Recibe la lista por props y solo PASA las funciones del padre a cada fila.
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
