// ==================================================================
// ARCHIVO  : api.js
// ROL      : INSTANCIA ÚNICA de Axios para hablar con la API de Django.
// ------------------------------------------------------------------
// LAB 12 - EJ 3 : axios.create con baseURL y timeout; la DIRECCIÓN DEL SERVIDOR
//                 se escribe SOLO AQUÍ (los componentes usan rutas cortas).
// LAB 12 - EJ 6 : textoError() convierte el ERROR 400 (err.response.data) en texto.
// ------------------------------------------------------------------
// USADO EN : ./practica/ListaPractica.jsx y ./components/PanelPrestadores.jsx
// ==================================================================
import axios from 'axios'

// INSTANCIA ÚNICA: la dirección del servidor se escribe solo aquí.
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 5000,
})

// CONVIERTE el error de Axios en un TEXTO para mostrar al usuario.
// Con respuesta de la API: 'campo: mensaje | campo: mensaje'. Sin respuesta: servidor caído.
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
