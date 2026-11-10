import { useState } from 'react'
import LibroCard from './LibroCard.jsx'

const formularioVacio = { titulo: '', autor: '', anio: '', copias: '1', categoria: '1' }

function LibroLista({ libros, categorias }) {
  const [lista, setLista] = useState(libros)
  const [busqueda, setBusqueda] = useState('')
  const [form, setForm] = useState(formularioVacio)
  const [error, setError] = useState('')

  const filtrados = lista.filter((libro) =>
    libro.titulo.toLowerCase().includes(busqueda.toLowerCase())
  )

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function manejarEnvio(e) {
    e.preventDefault()
    const anio = Number(form.anio)
    const anioActual = new Date().getFullYear()

    if (form.titulo.trim() === '' || form.autor.trim() === '') {
      setError('El título y el autor son obligatorios.')
      return
    }
    if (anio < 1450 || anio > anioActual) {
      setError('El año de publicación debe estar entre 1450 y el año actual.')
      return
    }

    const nuevo = {
      id: Math.max(0, ...lista.map((l) => l.id)) + 1,
      titulo: form.titulo.trim(),
      autor: form.autor.trim(),
      isbn: '',
      anio_publicacion: anio,
      copias: Number(form.copias),
      categoria: Number(form.categoria),
    }
    setLista([...lista, nuevo])
    setForm(formularioVacio)
    setError('')
  }

  return (
    <div>
      <form onSubmit={manejarEnvio} className="formulario">
        <h3>Agregar libro</h3>
        <input name="titulo" placeholder="Título" value={form.titulo} onChange={manejarCambio} />
        <input name="autor" placeholder="Autor" value={form.autor} onChange={manejarCambio} />
        <input name="anio" type="number" placeholder="Año de publicación" value={form.anio} onChange={manejarCambio} />
        <input name="copias" type="number" min="0" placeholder="Copias" value={form.copias} onChange={manejarCambio} />
        <select name="categoria" value={form.categoria} onChange={manejarCambio}>
          {categorias.map((c) => (
            <option key={c.id} value={c.id}>{c.nombre}</option>
          ))}
        </select>
        <button type="submit">Agregar</button>
        {error && <p className="error">{error}</p>}
      </form>

      <input
        type="text"
        placeholder="Buscar libro por título"
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />

      {filtrados.length === 0 ? (
        <p>Ningún libro coincide con la búsqueda</p>
      ) : (
        <ul>
          {filtrados.map((libro) => (
            <LibroCard
              key={libro.id}
              titulo={libro.titulo}
              autor={libro.autor}
              anio={libro.anio_publicacion}
              copias={libro.copias}
              categoria={categorias.find((c) => c.id === libro.categoria)?.nombre}
            />
          ))}
        </ul>
      )}
    </div>
  )
}

export default LibroLista