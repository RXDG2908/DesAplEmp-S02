// ==================================================================
// ARCHIVO  : Vet.jsx
// PARTE 1  : VET (reserva de citas de la veterinaria)
// ROL      : PANTALLA PRINCIPAL de la veterinaria.
// ------------------------------------------------------------------
// LAB 9 - EJ 4: JSX con EXPRESIONES -> precio de la consulta con IGV y toFixed(2).
// LAB 9 - EJ 5: LISTA con map() y KEY (hoy dentro de InsumoLista).
// LAB 9 - EJ 6: RENDERIZADO CONDICIONAL (hoy dentro de InsumoCard y CitaCard).
// LAB 9 - EJ 7: RELACIÓN 1:N con LISTAS ANIDADAS (citas con sus consumos).
// LAB 9 - EJ 8: ESTILOS con className (../App.css) y con style={{ }}.
// LAB 10 - EJ 1: este JSX se DIVIDIÓ en componentes (InsumoLista, CitaCard).
// ------------------------------------------------------------------
// DATOS    : ./datos.js (con la MISMA FORMA del JSON de la API del Lab 8)
// USA      : ./components/InsumoLista.jsx, ./components/CitaCard.jsx
// DOCS     : ../../docs/guiones/GUION-Lab09-Parte1.md
//            ../../docs/exposiciones/EXPOSICION_Lab09_Parte1.md
// ==================================================================
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

      {/* LAB 9 - EJ 8: ESTILO EN LÍNEA con style={{ }} */}
      <h2 style={{ color: '#1f5f5b' }}>Insumos</h2>
      <InsumoLista insumosIniciales={insumos} />

      {/* LAB 9 - EJ 7 / LAB 10 - EJ 5: una CitaCard por cita, con map() y key = id */}
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
