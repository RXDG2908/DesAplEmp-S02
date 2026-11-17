// ==================================================================
// GUIA: ARCHIVO  components/PrestamoItem.jsx
// LAB     : 10  -  PARTE 2 (biblioteca)
// QUE HACE : una linea de prestamo (libro - estado - multa); equivale a ./ConsumoItem.jsx de vet.
// ==================================================================
function PrestamoItem({ libro, estado, multa }) {
  return (
    <li>
      {libro} — {estado} — Multa: S/ {Number(multa).toFixed(2)}
    </li>
  )
}

export default PrestamoItem