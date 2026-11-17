import { useEffect } from 'react'

// Mensaje que desaparece solo a los 3 segundos
function Aviso({ mensaje, onTerminar }) {
  useEffect(() => {
    if (mensaje === '') return
    const temporizador = setTimeout(() => onTerminar(''), 3000)
    // Limpieza: cancela el temporizador si el componente se desmonta o cambia el mensaje
    return () => clearTimeout(temporizador)
  }, [mensaje, onTerminar])

  if (mensaje === '') return null
  return <p className="aviso">{mensaje}</p>
}

export default Aviso
