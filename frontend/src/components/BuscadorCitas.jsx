// ==================================================================
// ARCHIVO  : components/BuscadorCitas.jsx
// PARTE 1  : VET (panel de citas, primera versión del Lab 11)
// ------------------------------------------------------------------
// LAB 11 - EJ 13: BUSCADOR CONTROLADO POR EL PADRE (valor + onCambiar) que
//                 filtra las citas por mascota.
// ------------------------------------------------------------------
// USADO EN : ./PanelCitas.jsx
// ==================================================================
function BuscadorCitas({ valor, onCambiar }) {
  return (
    <input
      type="text"
      placeholder="Buscar por mascota"
      value={valor}
      onChange={(e) => onCambiar(e.target.value)}
    />
  )
}

export default BuscadorCitas
