// ==================================================================
// ARCHIVO  : components/BuscadorPrestadores.jsx
// PROYECTO : CHAMBA PE (proyecto integrador)
// ------------------------------------------------------------------
// LAB 11 - EJ 13: BUSCADOR CONTROLADO POR EL PADRE (valor + onCambiar).
// LAB 12 - EJ 13: el texto viaja a la API como ?search=.
// ------------------------------------------------------------------
// USADO EN : ./PanelPrestadores.jsx
// ==================================================================
function BuscadorPrestadores({ valor, onCambiar }) {
  return (
    <input
      type="text"
      placeholder="Buscar prestador por nombre"
      value={valor}
      onChange={(e) => onCambiar(e.target.value)}
    />
  )
}

export default BuscadorPrestadores
