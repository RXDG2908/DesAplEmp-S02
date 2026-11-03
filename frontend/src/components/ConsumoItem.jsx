// Un elemento anidado de la cita: un consumo de insumo (modelo intermedio N:M).
function ConsumoItem({ insumo, cantidad, subtotal }) {
  return (
    <li>
      {insumo} × {cantidad} — S/ {Number(subtotal).toFixed(2)}
    </li>
  )
}

export default ConsumoItem
