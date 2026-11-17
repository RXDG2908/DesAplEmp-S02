// ==================================================================
// GUIA: ARCHIVO  components/Tarjeta.jsx
// LAB     : 10 Ej.4 (children)  -  PARTE 1 (vet)
// QUE HACE : contenedor reutilizable con titulo; lo de entre sus etiquetas llega en `children`
//           (como un {% block %} de Django). Lo usa CitaCard.
// ==================================================================
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
