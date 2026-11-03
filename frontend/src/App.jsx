import './App.css'

const categorias = [
  { id: 1, nombre: 'Ciencia Ficción', descripcion: 'Relatos del futuro' },
  { id: 2, nombre: 'Novela', descripcion: 'Narrativa de ficción' },
  { id: 3, nombre: 'Historia', descripcion: 'Ensayo histórico' },
  { id: 4, nombre: 'Ciencia', descripcion: 'Divulgación científica' },
]

const libros = [
  { id: 1, titulo: 'Fundación', autor: 'Isaac Asimov', isbn: '9780000000002', anio_publicacion: 1951, copias: 3, categoria: 1 },
  { id: 2, titulo: 'La ciudad y los perros', autor: 'M. Vargas Llosa', isbn: '9788420471839', anio_publicacion: 1963, copias: 5, categoria: 2 },
  { id: 3, titulo: 'Los ríos profundos', autor: 'J. M. Arguedas', isbn: '9788437604350', anio_publicacion: 1958, copias: 1, categoria: 2 },
  { id: 4, titulo: 'Historia de la República', autor: 'J. Basadre', isbn: '9786124161070', anio_publicacion: 1939, copias: 3, categoria: 3 },
  { id: 5, titulo: 'Cosmos', autor: 'Carl Sagan', isbn: '9780345539434', anio_publicacion: 1980, copias: 5, categoria: 4 },
  { id: 6, titulo: 'Breve historia del tiempo', autor: 'Stephen Hawking', isbn: '9788498929355', anio_publicacion: 1988, copias: 0, categoria: 4 },
]

const socios = [
  {
    id: 1, nombre: 'Carlos Ramos', dni: '70123456',
    prestamos: [
      { id: 1, libro: 'La ciudad y los perros', estado: 'Activo', multa: '0.00' },
      { id: 2, libro: 'Historia de la República', estado: 'Devuelto', multa: '0.00' },
    ],
  },
  {
    id: 2, nombre: 'Elena Vega', dni: '71998877',
    prestamos: [
      { id: 3, libro: 'Los ríos profundos', estado: 'Atrasado', multa: '5.00' },
      { id: 4, libro: 'Cosmos', estado: 'Activo', multa: '0.00' },
    ],
  },
  {
    id: 3, nombre: 'Diego Salas', dni: '72345610',
    prestamos: [
      { id: 5, libro: 'Cosmos', estado: 'Devuelto', multa: '2.50' },
      { id: 6, libro: 'Breve historia del tiempo', estado: 'Atrasado', multa: '7.50' },
    ],
  },
  { id: 4, nombre: 'Rosa Medina', dni: '73456721', prestamos: [] },
]

function App() {
  const aplicacion = 'Biblioteca Comunitaria'
  const multaPorDia = 1.5
  const diasAtraso = 4

  return (
    <div className="contenedor">
      <h1 className="titulo">{aplicacion}</h1>
      <p>Multa por día: S/ {multaPorDia.toFixed(2)}</p>
      <p>Multa por {diasAtraso} días de atraso: S/ {(multaPorDia * diasAtraso).toFixed(2)}</p>

      <h2 style={{ color: '#5a3e2b' }}>Categorías</h2>
      <ul>
        {categorias.map((categoria) => (
          <li key={categoria.id}>
            {categoria.nombre} — {categoria.descripcion}
          </li>
        ))}
      </ul>

      <h2 style={{ color: '#5a3e2b' }}>Libros</h2>
      {libros.length === 0 ? (
        <p>No hay registros</p>
      ) : (
        <ul>
          {libros.map((libro) => (
            <li key={libro.id}>
              {libro.titulo} ({libro.anio_publicacion}) — {libro.autor} —{' '}
              {categorias.find((c) => c.id === libro.categoria).nombre} —{' '}
              {libro.copias === 0 ? (
                <span className="agotado">Agotado</span>
              ) : (
                `Copias: ${libro.copias}`
              )}
              {libro.copias === 1 && <strong> ¡Última copia!</strong>}
            </li>
          ))}
        </ul>
      )}

      <h2 style={{ color: '#5a3e2b' }}>Socios y sus préstamos</h2>
      {socios.map((socio) => (
        <div key={socio.id} className="tarjeta-socio">
          <h3>{socio.nombre} (DNI {socio.dni})</h3>
          {socio.prestamos.length === 0 ? (
            <p>Sin préstamos</p>
          ) : (
            <ul>
              {socio.prestamos.map((prestamo) => (
                <li key={prestamo.id}>
                  {prestamo.libro} — {prestamo.estado} — Multa: S/ {Number(prestamo.multa).toFixed(2)}
                </li>
              ))}
            </ul>
          )}
          <p>
            Total de multas: S/{' '}
            {socio.prestamos.reduce((suma, p) => suma + Number(p.multa), 0).toFixed(2)}
          </p>
        </div>
      ))}
    </div>
  )
}

export default App