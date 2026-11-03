import { useState } from 'react'
import InsumoCard from './InsumoCard.jsx'

// Lista con estado: busqueda controlada y formulario que agrega un insumo.
// Regla de la API (Semana 8, validate_stock): el stock inicial debe ser >= 1.
function InsumoLista({ insumosIniciales }) {
  const [insumos, setInsumos] = useState(insumosIniciales)
  const [busqueda, setBusqueda] = useState('')
  const [nombre, setNombre] = useState('')
  const [stock, setStock] = useState('')
  const [error, setError] = useState('')

  const visibles = insumos.filter((i) =>
    i.nombre.toLowerCase().includes(busqueda.toLowerCase()),
  )

  const enviar = (e) => {
    e.preventDefault()
    if (nombre.trim() === '') {
      setError('El nombre es obligatorio.')
      return
    }
    if (Number(stock) < 1) {
      setError('El stock inicial debe ser de al menos 1 unidad.')
      return
    }
    const nuevo = { id: Date.now(), nombre: nombre.trim(), unidad: 'unidad', stock: Number(stock) }
    setInsumos([...insumos, nuevo])
    setNombre('')
    setStock('')
    setError('')
  }

  return (
    <div>
      <input
        type="text"
        placeholder="Buscar insumo..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />
      {visibles.length === 0 ? (
        <p>Ningún insumo coincide con la búsqueda</p>
      ) : (
        <ul>
          {visibles.map((insumo) => (
            <InsumoCard key={insumo.id} nombre={insumo.nombre} unidad={insumo.unidad} stock={insumo.stock} />
          ))}
        </ul>
      )}

      <form onSubmit={enviar}>
        <input
          type="text"
          placeholder="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />{' '}
        <input
          type="number"
          placeholder="Stock"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
        />{' '}
        <button type="submit">Agregar insumo</button>
        {error && <p className="sin-stock">{error}</p>}
      </form>
    </div>
  )
}

export default InsumoLista
