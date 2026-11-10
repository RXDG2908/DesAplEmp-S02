import './App.css'
import Vet from './Vet.jsx'
import Panel from './components/Panel.jsx'
import LibroLista from './components/LibroLista.jsx'
import SocioCard from './components/SocioCard.jsx'
import { categorias, libros, socios } from './datosBiblioteca.js'

function App() {
  const aplicacion = 'Biblioteca Comunitaria'
  const multaPorDia = 1.5
  const diasAtraso = 4

  return (
    <div className="contenedor">
      <Vet />
      <h1 className="titulo">{aplicacion}</h1>
      <p>Multa por día: S/ {multaPorDia.toFixed(2)}</p>
      <p>Multa por {diasAtraso} días de atraso: S/ {(multaPorDia * diasAtraso).toFixed(2)}</p>

      <Panel titulo="Categorías">
        <ul>
          {categorias.map((categoria) => (
            <li key={categoria.id}>
              {categoria.nombre} — {categoria.descripcion}
            </li>
          ))}
        </ul>
      </Panel>

      <Panel titulo="Libros">
        <LibroLista libros={libros} categorias={categorias} />
      </Panel>

      <Panel titulo="Socios y sus préstamos">
        {socios.map((socio) => (
          <SocioCard
            key={socio.id}
            nombre={socio.nombre}
            dni={socio.dni}
            prestamos={socio.prestamos}
          />
        ))}
      </Panel>
    </div>
  )
}

export default App