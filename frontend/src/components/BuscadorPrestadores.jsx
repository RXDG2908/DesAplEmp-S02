// Filtro de texto controlado: el valor y el cambio los maneja el padre
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
