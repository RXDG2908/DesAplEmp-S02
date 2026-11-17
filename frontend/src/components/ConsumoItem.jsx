// ==================================================================
// GUIA: ARCHIVO  components/ConsumoItem.jsx
// LAB     : 10 Ej.5  -  PARTE 1 (vet)
// QUE HACE : una linea de consumo (insumo x cantidad - subtotal). Usado en ./CitaCard.jsx.
// ==================================================================
// Un elemento anidado de la cita: un consumo de insumo (modelo intermedio N:M).
function ConsumoItem({ insumo, cantidad, subtotal }) {
  return (
    <li>
      {insumo} × {cantidad} — S/ {Number(subtotal).toFixed(2)}
    </li>
  )
}

export default ConsumoItem
