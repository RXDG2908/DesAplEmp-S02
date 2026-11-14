function Buscador({ valor, onCambiar }) {
  return (
    <input
      type="text"
      placeholder="Buscar producto"
      value={valor}
      onChange={(e) => onCambiar(e.target.value)}
    />
  )
}

export default Buscador
