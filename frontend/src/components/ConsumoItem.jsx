// ==================================================================
// ARCHIVO  : components/ConsumoItem.jsx
// PARTE 1  : VET (reserva de citas de la veterinaria)
// ROL      : UNA LÍNEA de consumo -> insumo × cantidad — subtotal.
// ------------------------------------------------------------------
// LAB 10 - EJ 5: ELEMENTO ANIDADO de la cita (un registro del MODELO INTERMEDIO N:M).
// ------------------------------------------------------------------
// USADO EN : ./CitaCard.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 10 - EJ 5 .... línea 13
// ==================================================================
function ConsumoItem({ insumo, cantidad, subtotal }) {
  return (
    <li>
      {insumo} × {cantidad} — S/ {Number(subtotal).toFixed(2)}
    </li>
  )
}

export default ConsumoItem
