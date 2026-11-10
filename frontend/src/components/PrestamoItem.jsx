function PrestamoItem({ libro, estado, multa }) {
  return (
    <li>
      {libro} — {estado} — Multa: S/ {Number(multa).toFixed(2)}
    </li>
  )
}

export default PrestamoItem