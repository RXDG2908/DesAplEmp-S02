import { useState } from 'react'

const formularioVacio = { nombres: '', apellidos: '', rubro: 'Gasfitería', tarifa: '' }

// Formulario controlado para alta y edición. Si recibe un prestador, parte con sus datos
function PrestadorForm({ prestador, onGuardar, onCancelar }) {
  const [form, setForm] = useState(
    prestador
      ? { nombres: prestador.nombres, apellidos: prestador.apellidos, rubro: prestador.rubro, tarifa: String(prestador.tarifa) }
      : formularioVacio
  )
  const [error, setError] = useState('')

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function manejarEnvio(e) {
    e.preventDefault()
    // Validación previa en el navegador; la API vuelve a validar y responde 400 si algo falla
    if (form.nombres.trim() === '' || form.apellidos.trim() === '') {
      setError('Los nombres y los apellidos son obligatorios.')
      return
    }
    const mensaje = await onGuardar({
      nombres: form.nombres.trim(),
      apellidos: form.apellidos.trim(),
      rubro: form.rubro,
      tarifa: form.tarifa,
    })
    if (mensaje === '') {
      if (!prestador) setForm(formularioVacio)
      setError('')
    } else {
      setError(mensaje)
    }
  }

  return (
    <form onSubmit={manejarEnvio} className="formulario">
      <h3>{prestador ? 'Editar prestador' : 'Registrar prestador'}</h3>
      <input name="nombres" placeholder="Nombres" value={form.nombres} onChange={manejarCambio} />
      <input name="apellidos" placeholder="Apellidos" value={form.apellidos} onChange={manejarCambio} />
      <select name="rubro" value={form.rubro} onChange={manejarCambio}>
        <option>Gasfitería</option>
        <option>Electricidad</option>
        <option>Costura</option>
        <option>Carpintería</option>
        <option>Primeros auxilios</option>
      </select>
      <input name="tarifa" type="number" placeholder="Tarifa (S/)" value={form.tarifa} onChange={manejarCambio} />
      <button type="submit">{prestador ? 'Actualizar' : 'Guardar'}</button>
      {prestador && (
        <button type="button" onClick={onCancelar}>
          Cancelar
        </button>
      )}
      {error && <p className="error">{error}</p>}
    </form>
  )
}

export default PrestadorForm
