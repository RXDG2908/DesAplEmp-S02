// ==================================================================
// ARCHIVO  : components/Tarjeta.jsx
// PARTE 1  : VET (reserva de citas de la veterinaria)
// ROL      : CONTENEDOR REUTILIZABLE con título.
// ------------------------------------------------------------------
// LAB 10 - EJ 4: recibe titulo y CHILDREN (lo que se escribe ENTRE sus etiquetas),
//                igual que un {% block %} de los Templates de Django.
// ------------------------------------------------------------------
// USADO EN : ./CitaCard.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 10 - EJ 4 .... línea 18
// ==================================================================
function Tarjeta({ titulo, children }) {
  return (
    <div className="tarjeta-cita">
      <h3>{titulo}</h3>
      {children}
    </div>
  )
}

export default Tarjeta
