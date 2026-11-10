import PrestamoItem from './PrestamoItem.jsx'

function SocioCard({ nombre, dni, prestamos }) {
  const totalMultas = prestamos.reduce((suma, p) => suma + Number(p.multa), 0)

  return (
    <div className="tarjeta-socio">
      <h3>{nombre} (DNI {dni})</h3>
      {prestamos.length === 0 ? (
        <p>Sin préstamos</p>
      ) : (
        <ul>
          {prestamos.map((prestamo) => (
            <PrestamoItem
              key={prestamo.id}
              libro={prestamo.libro}
              estado={prestamo.estado}
              multa={prestamo.multa}
            />
          ))}
        </ul>
      )}
      <p>Total de multas: S/ {totalMultas.toFixed(2)}</p>
    </div>
  )
}

export default SocioCard