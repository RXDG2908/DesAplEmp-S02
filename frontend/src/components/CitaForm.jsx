import { useState } from 'react'

const formularioVacio = { mascota: '', dueno: '', servicio: 'Consulta', hora: '' }

// Formulario controlado: valida y entrega la cita nueva al padre con onGuardar
function CitaForm({ onGuardar }) {
  const [form, setForm] = useState(formularioVacio)
  const [error, setError] = useState('')

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function manejarEnvio(e) {
    e.preventDefault()
    if (form.mascota.trim() === '' || form.dueno.trim() === '') {
      setError('La mascota y el dueño son obligatorios.')
      return
    }
    if (form.hora === '' || form.hora < '08:00' || form.hora > '18:00') {
      setError('La hora debe estar entre 08:00 y 18:00.')
      return
    }
    onGuardar({
      mascota: form.mascota.trim(),
      dueno: form.dueno.trim(),
      servicio: form.servicio,
      hora: form.hora,
    })
    setForm(formularioVacio)
    setError('')
  }

  return (
    <form onSubmit={manejarEnvio} className="formulario">
      <h3>Agregar cita</h3>
      <input name="mascota" placeholder="Mascota" value={form.mascota} onChange={manejarCambio} />
      <input name="dueno" placeholder="Dueño" value={form.dueno} onChange={manejarCambio} />
      <select name="servicio" value={form.servicio} onChange={manejarCambio}>
        <option>Consulta</option>
        <option>Vacunacion</option>
        <option>Cirugia</option>
      </select>
      <input name="hora" type="time" value={form.hora} onChange={manejarCambio} />
      <button type="submit">Guardar</button>
      {error && <p className="error">{error}</p>}
    </form>
  )
}

export default CitaForm
