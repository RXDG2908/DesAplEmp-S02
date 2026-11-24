// ==================================================================
// ARCHIVO  : components/CitaListado.jsx
// PARTE 1  : VET (panel de citas, primera versión del Lab 11)
// ROL      : TABLA de citas del panel (una CitaFila por cita).
// ------------------------------------------------------------------
// LAB 11 - EJ 10: TABLA de citas; recibe la lista por props y dibuja una CitaFila
//                 por cita con map() y key = id.
// LAB 11 - EJ 13: muestra un MENSAJE cuando la búsqueda no da resultados.
// ------------------------------------------------------------------
// USADO EN : ./PanelCitas.jsx  ·  USA: ./CitaFila.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 10 ... línea 37
//   LAB 11 - EJ 13 ... línea 21
// ==================================================================
import CitaFila from './CitaFila.jsx'

// Recibe la lista por props y solo PASA las funciones del padre a cada fila.
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
