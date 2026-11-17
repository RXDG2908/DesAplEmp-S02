// ==================================================================
// ARCHIVO  : components/CitaCard.jsx
// PARTE 1  : VET (reserva de citas de la veterinaria)
// ROL      : UNA CITA dentro de <Tarjeta> con la lista de sus consumos.
// ------------------------------------------------------------------
// LAB 10 - EJ 4: usa el CONTENEDOR <Tarjeta> (lo de adentro llega como children).
// LAB 10 - EJ 5: COMPONENTE DENTRO DE COMPONENTE -> un ConsumoItem por consumo
//                (relación 1:N) y el TOTAL calculado con reduce().
// ------------------------------------------------------------------
// USADO EN : ../Vet.jsx  ·  USA: ./Tarjeta.jsx y ./ConsumoItem.jsx
// ==================================================================
import Tarjeta from './Tarjeta.jsx'
import ConsumoItem from './ConsumoItem.jsx'

// LAB 10 - EJ 5: RELACIÓN 1:N con LISTAS ANIDADAS. consumos = [] es un VALOR POR DEFECTO.
// La prop de la API "dueno" se RENOMBRA a "propietario" al desestructurar.
function CitaCard({ mascota, dueno: propietario, servicio, hora, estado, veterinario, consumos = [] }) {
  // LAB 10 - EJ 5: TOTAL DERIVADO; Number() convierte el subtotal que la API envía como texto.
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
