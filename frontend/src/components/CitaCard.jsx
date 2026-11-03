import Tarjeta from './Tarjeta.jsx'
import ConsumoItem from './ConsumoItem.jsx'

// Relacion 1:N con listas anidadas: la cita usa ConsumoItem por cada consumo.
// El prop de la API "dueno" se recibe como "propietario" (nombre propio del componente).
function CitaCard({ mascota, dueno: propietario, servicio, hora, estado, veterinario, consumos = [] }) {
  const total = consumos.reduce((suma, c) => suma + Number(c.subtotal), 0)

  return (
    <Tarjeta titulo={`${mascota} (${propietario}) — ${servicio}`}>
      <p>
        {hora} — {veterinario} — {estado}
      </p>
      {consumos.length === 0 ? (
        <p>Sin consumos</p>
      ) : (
        <ul>
          {consumos.map((consumo) => (
            <ConsumoItem
              key={consumo.insumo}
              insumo={consumo.insumo}
              cantidad={consumo.cantidad}
              subtotal={consumo.subtotal}
            />
          ))}
        </ul>
      )}
      <p>Total de consumos: S/ {total.toFixed(2)}</p>
    </Tarjeta>
  )
}

export default CitaCard
