import InsumoCard from './InsumoCard.jsx'

// Recibe la lista ya filtrada y entrega cada insumo a su tarjeta
function Catalogo({ insumos, onAgregar }) {
  if (insumos.length === 0) {
    return <p>No hay insumos que coincidan</p>
  }

  return (
    <ul>
      {insumos.map((insumo) => (
        <InsumoCard key={insumo.id} insumo={insumo} onAgregar={onAgregar} />
      ))}
    </ul>
  )
}

export default Catalogo
