import axios from 'axios'

// Instancia única: la dirección del servidor se escribe solo aquí
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 5000,
})

// Convierte el error de Axios en un texto para mostrar al usuario
export function textoError(err) {
  const datos = err.response && err.response.data
  if (datos && typeof datos === 'object') {
    return Object.entries(datos)
      .map(([campo, mensajes]) => `${campo}: ${[].concat(mensajes).join(' ')}`)
      .join(' | ')
  }
  return 'No se pudo conectar con el servidor.'
}

export default api
