// ==================================================================
// ARCHIVO  : practica_lucas/ListaLibros.jsx
// PARTE 2  : BIBLIOTECA (Lucas) -> libros leidos desde la API de Django (Lab 12)
// ------------------------------------------------------------------
// LAB 12 - EJ 4: GET con await api.get(...) dentro de un useEffect; lista con map() y key = id.
// LAB 12 - EJ 5: estados CARGANDO, ERROR y LISTA VACIA con try / catch / finally.
// LAB 12 - EJ 6: POST con formulario controlado; muestra el ERROR 400 de validate_anio_publicacion.
// LAB 12 - EJ 7: DELETE (204) con filter() y PATCH (+1 copia, 200) con map().
// LAB 12 - EJ 8: BUSQUEDA enviada como ?search= y efecto con dependencia [buscar].
// ------------------------------------------------------------------
// USADO EN : ../App.jsx (vista 'libros')   API: /api/biblioteca/libros/
// ==================================================================
import { useEffect, useState } from 'react'
import api, { textoError } from '../api.js'

const formularioVacio = {
  titulo: '',
  autor: '',
  isbn: '',
  anio_publicacion: '',
  copias: '',
  categoria: '',
}

function ListaLibros() {
  const [libros, setLibros] = useState([])
  const [categorias, setCategorias] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(false)
  const [buscar, setBuscar] = useState('')
  const [form, setForm] = useState(formularioVacio)
  const [errorForm, setErrorForm] = useState('')

  // EJ 4 y 8: la peticion va en un EFECTO (se ejecuta DESPUES de dibujar y cada vez que
  // cambia buscar). La funcion del efecto NO es async: se declara cargar() aparte.
  useEffect(() => {
    async function cargar() {
      try {
        const respuesta = await api.get('/biblioteca/libros/', { params: { search: buscar } })
        setLibros(respuesta.data)
        setError(false)
      } catch (err) {
        console.log('Error al cargar los libros:', err.message)
        setError(true)
      } finally {
        setCargando(false)
      }
    }
    cargar()
  }, [buscar])

  // Categorias para el <select> del formulario (una sola vez: dependencias []).
  useEffect(() => {
    async function cargarCategorias() {
      try {
        const respuesta = await api.get('/biblioteca/categorias/')
        setCategorias(respuesta.data)
      } catch (err) {
        console.log('Error al cargar las categorias:', err.message)
      }
    }
    cargarCategorias()
  }, [])

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  // EJ 6: POST -> 201 y se agrega respuesta.data con un arreglo NUEVO; 400 -> mensaje en pantalla.
  async function crear(e) {
    e.preventDefault()
    try {
      const respuesta = await api.post('/biblioteca/libros/', {
        titulo: form.titulo,
        autor: form.autor,
        isbn: form.isbn,
        anio_publicacion: Number(form.anio_publicacion),
        copias: Number(form.copias),
        categoria: Number(form.categoria),
      })
      setLibros([...libros, respuesta.data])
      setForm(formularioVacio)
      setErrorForm('')
    } catch (err) {
      setErrorForm(textoError(err))
    }
  }

  // EJ 7: DELETE -> 204 y se quita del estado con filter().
  async function eliminar(id) {
    try {
      await api.delete(`/biblioteca/libros/${id}/`)
      setLibros(libros.filter((l) => l.id !== id))
      setErrorForm('')
    } catch (err) {
      setErrorForm(textoError(err))
    }
  }

  // EJ 7: PATCH -> 200 y se reemplaza el registro en el estado con map().
  async function sumarCopia(libro) {
    try {
      const respuesta = await api.patch(`/biblioteca/libros/${libro.id}/`, {
        copias: libro.copias + 1,
      })
      setLibros(libros.map((l) => (l.id === libro.id ? respuesta.data : l)))
      setErrorForm('')
    } catch (err) {
      setErrorForm(textoError(err))
    }
  }

  return (
    <div className="seccion-vet">
      <h2>Libros desde la API de Django</h2>

      <form onSubmit={crear} className="formulario">
        <h3>Agregar libro</h3>
        <input name="titulo" placeholder="Titulo" value={form.titulo} onChange={manejarCambio} />
        <input name="autor" placeholder="Autor" value={form.autor} onChange={manejarCambio} />
        <input name="isbn" placeholder="ISBN" value={form.isbn} onChange={manejarCambio} />
        <input
          name="anio_publicacion"
          type="number"
          placeholder="Año de publicación"
          value={form.anio_publicacion}
          onChange={manejarCambio}
        />
        <input
          name="copias"
          type="number"
          placeholder="Copias"
          value={form.copias}
          onChange={manejarCambio}
        />
        <select name="categoria" value={form.categoria} onChange={manejarCambio}>
          <option value="">Categoría...</option>
          {categorias.map((c) => (
            <option key={c.id} value={c.id}>
              {c.nombre}
            </option>
          ))}
        </select>
        <button type="submit">Guardar</button>
        {errorForm && <p className="error">{errorForm}</p>}
      </form>

      <input
        type="text"
        placeholder="Buscar libro"
        value={buscar}
        onChange={(e) => setBuscar(e.target.value)}
      />

      {cargando && <p>Cargando...</p>}
      {error && <p className="error">No se pudo cargar la lista</p>}
      {!cargando && !error && libros.length === 0 && <p>No hay libros registrados</p>}
      <ul>
        {libros.map((libro) => (
          <li key={libro.id}>
            {libro.titulo} ({libro.anio_publicacion}) — {libro.autor} — Copias: {libro.copias}{' '}
            <button onClick={() => sumarCopia(libro)}>+1 copia</button>{' '}
            <button onClick={() => eliminar(libro.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ListaLibros
