import { insumos, citas } from './datos.js'
import InsumoLista from './components/InsumoLista.jsx'
import CitaCard from './components/CitaCard.jsx'

function Vet() {
  const aplicacion = 'Veterinaria - Reserva de citas'
  const precioConsulta = 40
  const igv = 0.18

  return (
    <section className="seccion-vet">
      <h1 className="titulo">{aplicacion}</h1>
      <p>Consulta base: S/ {precioConsulta.toFixed(2)}</p>
      <p>Consulta con IGV ({igv * 100}%): S/ {(precioConsulta * (1 + igv)).toFixed(2)}</p>

      <h2 style={{ color: '#1f5f5b' }}>Insumos</h2>
      <InsumoLista insumosIniciales={insumos} />

      <h2 style={{ color: '#1f5f5b' }}>Citas y sus consumos</h2>
      {citas.map((cita) => (
        <CitaCard
          key={cita.id}
          mascota={cita.mascota}
          dueno={cita.dueno}
          servicio={cita.servicio}
          hora={cita.hora}
          estado={cita.estado}
          veterinario={cita.veterinario.nombre}
          consumos={cita.consumos}
        />
      ))}
    </section>
  )
}

export default Vet
