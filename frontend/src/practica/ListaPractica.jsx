// ==================================================================
// ARCHIVO  : practica/ListaPractica.jsx
// PARTE 1  : VET -> insumos leídos desde la API de Django (práctica del Lab 12)
// ------------------------------------------------------------------
// LAB 12 - EJ 4: GET con await api.get(...) dentro de un useEffect; lista con map() y key.
// LAB 12 - EJ 5: estados CARGANDO, ERROR y LISTA VACÍA con try / catch / finally.
// LAB 12 - EJ 6: POST con formulario controlado; muestra el ERROR 400 de validate_stock.
// LAB 12 - EJ 7: DELETE (204) con filter() y PATCH (+1 stock, 200) con map().
// LAB 12 - EJ 8: BÚSQUEDA enviada como ?search= y efecto con dependencia [buscar].
// ------------------------------------------------------------------
// USADO EN : ../App.jsx (vista 'api')
// ==================================================================
import { useEffect, useState } from 'react'
import api, { textoError } from '../api.js'

const formularioVacio = { nombre: '', unidad: 'unidad', stock: '' }

// INSUMOS de la API de Django: LISTA, ALTA, CAMBIO DE STOCK y BAJA.
function ListaPractica() {
  const [insumos, setInsumos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(false)
  const [buscar, setBuscar] = useState('')
  const [form, setForm] = useState(formularioVacio)
  const [errorForm, setErrorForm] = useState('')

  // LAB 12 - EJ 4 y 8: la petición va en un EFECTO -> se ejecuta DESPUÉS DE DIBUJAR y cada
  // vez que cambia buscar. La función del efecto NO es async: se declara cargar() aparte.
  useEffect(() => {
    async function cargar() {
      try {
        const respuesta = await api.get('/insumos/', { params: { search: buscar } })
        setInsumos(respuesta.data)
        setError(false)
      } catch (err) {
        console.log('Error al cargar los insumos:', err.message)
        setError(true)
      } finally {
        setCargando(false)
      }
    }
    cargar()
  }, [buscar])

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function crear(e) {
    e.preventDefault()
    try {
      const respuesta = await api.post('/insumos/', {
        nombre: form.nombre,
        unidad: form.unidad,
        stock: Number(form.stock),
      })
      setInsumos([...insumos, respuesta.data])
      setForm(formularioVacio)
      setErrorForm('')
    } catch (err) {
      setErrorForm(textoError(err))
    }
  }

  async function eliminar(id) {
    try {
      await api.delete(`/insumos/${id}/`)
      setInsumos(insumos.filter((i) => i.id !== id))
    } catch (err) {
      setErrorForm(textoError(err))
    }
  }

  async function sumarStock(insumo) {
    try {
      const respuesta = await api.patch(`/insumos/${insumo.id}/`, { stock: insumo.stock + 1 })
      setInsumos(insumos.map((i) => (i.id === insumo.id ? respuesta.data : i)))
    } catch (err) {
      setErrorForm(textoError(err))
    }
  }

  return (
    <div className="seccion-vet">
      <h2>Insumos desde la API de Django</h2>

      <form onSubmit={crear} className="formulario">
        <h3>Agregar insumo</h3>
        <input name="nombre" placeholder="Nombre" value={form.nombre} onChange={manejarCambio} />
        <input name="unidad" placeholder="Unidad" value={form.unidad} onChange={manejarCambio} />
        <input name="stock" type="number" placeholder="Stock" value={form.stock} onChange={manejarCambio} />
        <button type="submit">Guardar</button>
        {errorForm && <p className="error">{errorForm}</p>}
      </form>

      <input
        type="text"
        placeholder="Buscar insumo"
        value={buscar}
        onChange={(e) => setBuscar(e.target.value)}
      />

      {cargando && <p>Cargando...</p>}
      {error && <p className="error">No se pudo cargar la lista</p>}
      {!cargando && !error && insumos.length === 0 && <p>No hay insumos registrados</p>}
      <ul>
        {insumos.map((insumo) => (
          <li key={insumo.id}>
            {insumo.nombre} — {insumo.unidad} — Stock: {insumo.stock}{' '}
            <button onClick={() => sumarStock(insumo)}>+1 stock</button>{' '}
            <button onClick={() => eliminar(insumo.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ListaPractica
