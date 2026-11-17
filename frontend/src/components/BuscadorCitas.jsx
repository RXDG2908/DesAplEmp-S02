// Filtro de texto controlado: el valor y el cambio los maneja el padre
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
