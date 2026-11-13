import { useState } from 'react'

const formularioVacio = { nombres: '', apellidos: '', rubro: 'Gasfitería', tarifa: '' }

// Formulario controlado: valida y entrega el prestador nuevo al padre con onGuardar
function PrestadorForm({ onGuardar }) {
  const [form, setForm] = useState(formularioVacio)
  const [error, setError] = useState('')

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function manejarEnvio(e) {
    e.preventDefault()
    if (form.nombres.trim() === '' || form.apellidos.trim() === '') {
      setError('Los nombres y los apellidos son obligatorios.')
      return
    }
    if (Number(form.tarifa) <= 0) {
      setError('La tarifa debe ser un número mayor que cero.')
      return
    }
    onGuardar({
      nombres: form.nombres.trim(),
      apellidos: form.apellidos.trim(),
      rubro: form.rubro,
      tarifa: Number(form.tarifa).toFixed(2),
    })
    setForm(formularioVacio)
    setError('')
  }

  return (
    <form onSubmit={manejarEnvio} className="formulario">
      <h3>Registrar prestador</h3>
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
      <button type="submit">Guardar</button>
      {error && <p className="error">{error}</p>}
    </form>
  )
}

export default PrestadorForm
