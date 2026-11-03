// Contenedor reutilizable: recibe un titulo y children (lo que se escribe entre sus etiquetas).
function Tarjeta({ titulo, children }) {
  return (
    <div className="tarjeta-cita">
      <h3>{titulo}</h3>
      {children}
    </div>
  )
}

export default Tarjeta
