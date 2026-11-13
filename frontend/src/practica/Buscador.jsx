// Campo de texto controlado: el valor vive en el padre
function Buscador({ valor, onCambiar }) {
  return (
    <input
      type="text"
      placeholder="Buscar insumo"
      value={valor}
      onChange={(e) => onCambiar(e.target.value)}
    />
  )
}

export default Buscador
