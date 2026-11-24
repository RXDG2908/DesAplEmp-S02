// ==================================================================
// ARCHIVO  : components/InsumoLista.jsx
// PARTE 1  : VET (reserva de citas de la veterinaria)
// ROL      : LISTA de InsumoCard con BUSCADOR y FORMULARIO de alta.
// ------------------------------------------------------------------
// LAB 10 - EJ 3: ARMA LA LISTA pasando a cada InsumoCard sus datos por props.
// LAB 10 - EJ 7: CAMPO CONTROLADO (value + onChange) que FILTRA por nombre
//                sin distinguir mayúsculas.
// LAB 10 - EJ 8: FORMULARIO CONTROLADO con onSubmit + preventDefault que VALIDA
//                y agrega el insumo con un ARREGLO NUEVO (spread, sin push).
// NOTA     : el insumo nuevo SOLO VIVE en el estado de React; se pierde al
//            recargar (en el Lab 12 se guarda en la API).
// ------------------------------------------------------------------
// USADO EN : ../Vet.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 10 - EJ 3 .... línea 68
//   LAB 10 - EJ 7 .... línea 32
//   LAB 10 - EJ 8 .... líneas 24, 37
// ==================================================================
import { useState } from 'react'
import InsumoCard from './InsumoCard.jsx'

// LAB 10 - EJ 8: la validación repite la REGLA de la API (Lab 8, validate_stock): stock inicial >= 1.
function InsumoLista({ insumosIniciales }) {
  const [insumos, setInsumos] = useState(insumosIniciales)
  const [busqueda, setBusqueda] = useState('')
  const [nombre, setNombre] = useState('')
  const [stock, setStock] = useState('')
  const [error, setError] = useState('')

  // LAB 10 - EJ 7: DATO DERIVADO -> la lista filtrada se calcula en cada dibujo.
  const visibles = insumos.filter((i) =>
    i.nombre.toLowerCase().includes(busqueda.toLowerCase()),
  )

  // LAB 10 - EJ 8: preventDefault() evita que el navegador RECARGUE la página al enviar.
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
