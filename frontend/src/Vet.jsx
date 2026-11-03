// Interfaz de la veterinaria (app `vet`). Los datos se escriben a mano con la
// misma forma que devuelve la API de la Semana 8 (/api/insumos/ y /api/citas/):
// los decimales llegan como texto y la cita trae veterinario, ficha y consumos.

const insumos = [
  { id: 1, nombre: 'Jeringa 5ml', unidad: 'unidad', stock: 100 },
  { id: 2, nombre: 'Vacuna antirrabica', unidad: 'dosis', stock: 12 },
  { id: 3, nombre: 'Suero fisiologico', unidad: 'frasco', stock: 1 },
  { id: 4, nombre: 'Antiparasitario', unidad: 'tableta', stock: 0 },
  { id: 5, nombre: 'Gasa esteril', unidad: 'paquete', stock: 40 },
]

const citas = [
  {
    id: 1, mascota: 'Firulais', dueno: 'Marta Quispe', servicio: 'Vacunacion',
    fecha: '2026-10-20', hora: '09:00', estado: 'Atendida',
    veterinario: { id: 1, nombre: 'Dra. Ana Torres', colegiatura: 'CMVP-1234', especialidad: 'Medicina general' },
    ficha: { peso_kg: '12.50', diagnostico: 'Sano', tratamiento: 'Vacuna antirrabica', proximo_control: '2027-10-20' },
    consumos: [
      { insumo: 'Jeringa 5ml', cantidad: 1, precio_unitario: '1.50', subtotal: '1.50' },
      { insumo: 'Vacuna antirrabica', cantidad: 1, precio_unitario: '25.00', subtotal: '25.00' },
    ],
  },
  {
    id: 2, mascota: 'Michi', dueno: 'Jorge Paredes', servicio: 'Consulta',
    fecha: '2026-11-05', hora: '10:30', estado: 'Confirmada',
    veterinario: { id: 2, nombre: 'Dr. Luis Gamarra', colegiatura: 'CMVP-5678', especialidad: 'Felinos' },
    ficha: null,
    consumos: [],
  },
  {
    id: 3, mascota: 'Rocky', dueno: 'Carla Rios', servicio: 'Cirugia',
    fecha: '2026-11-08', hora: '15:00', estado: 'Pendiente',
    veterinario: { id: 1, nombre: 'Dra. Ana Torres', colegiatura: 'CMVP-1234', especialidad: 'Medicina general' },
    ficha: null,
    consumos: [
      { insumo: 'Suero fisiologico', cantidad: 2, precio_unitario: '8.00', subtotal: '16.00' },
      { insumo: 'Gasa esteril', cantidad: 3, precio_unitario: '2.50', subtotal: '7.50' },
    ],
  },
  {
    id: 4, mascota: 'Luna', dueno: 'Pedro Soto', servicio: 'Consulta',
    fecha: '2026-11-12', hora: '11:15', estado: 'Pendiente',
    veterinario: { id: 2, nombre: 'Dr. Luis Gamarra', colegiatura: 'CMVP-5678', especialidad: 'Felinos' },
    ficha: null,
    consumos: [],
  },
]

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
      {insumos.length === 0 ? (
        <p>No hay registros</p>
      ) : (
        <ul>
          {insumos.map((insumo) => (
            <li key={insumo.id}>
              {insumo.nombre} ({insumo.unidad}) —{' '}
              {insumo.stock === 0 ? (
                <span className="sin-stock">Sin stock</span>
              ) : (
                `Stock: ${insumo.stock}`
              )}
              {insumo.stock === 1 && <strong> ¡Última unidad!</strong>}
            </li>
          ))}
        </ul>
      )}

      <h2 style={{ color: '#1f5f5b' }}>Citas y sus consumos</h2>
      {citas.length === 0 ? (
        <p>No hay registros</p>
      ) : (
        citas.map((cita) => (
          <div key={cita.id} className="tarjeta-cita">
            <h3>
              {cita.mascota} ({cita.dueno}) — {cita.servicio}
            </h3>
            <p>
              {cita.fecha} {cita.hora} — {cita.veterinario.nombre} — {cita.estado}
              {cita.estado === 'Pendiente' && <strong> Por confirmar</strong>}
            </p>
            {cita.ficha ? (
              <p>
                Ficha: {Number(cita.ficha.peso_kg).toFixed(2)} kg — {cita.ficha.diagnostico}
              </p>
            ) : (
              <p>Sin ficha clínica</p>
            )}
            {cita.consumos.length === 0 ? (
              <p>Sin consumos</p>
            ) : (
              <ul>
                {cita.consumos.map((consumo) => (
                  <li key={consumo.insumo}>
                    {consumo.insumo} × {consumo.cantidad} — S/ {Number(consumo.subtotal).toFixed(2)}
                  </li>
                ))}
              </ul>
            )}
            <p>
              Total de consumos: S/{' '}
              {cita.consumos.reduce((suma, c) => suma + Number(c.subtotal), 0).toFixed(2)}
            </p>
          </div>
        ))
      )}
    </section>
  )
}

export default Vet
