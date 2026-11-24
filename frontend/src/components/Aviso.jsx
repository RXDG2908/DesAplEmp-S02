// ==================================================================
// ARCHIVO  : components/Aviso.jsx
// ROL      : MENSAJE TEMPORAL que DESAPARECE SOLO a los 3 segundos.
// ------------------------------------------------------------------
// LAB 11 - EJ 8 : en la práctica muestra 'Agregado: <nombre>'.
// LAB 11 - EJ 13: en los paneles (VET y CHAMBA PE) avisa altas y cambios.
// ------------------------------------------------------------------
// USADO EN : ../practica/Practica.jsx, ./PanelCitas.jsx, ./PanelPrestadores.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 8 .... línea 18
//   LAB 11 - EJ 13 ... línea 18
// ==================================================================
import { useEffect } from 'react'

// El mensaje vive en el PADRE; al terminar, Aviso lo BORRA con onTerminar('').
function Aviso({ mensaje, onTerminar }) {
  // LAB 11 - EJ 8: useEffect + setTimeout; se repite cada vez que CAMBIA el mensaje.
  useEffect(() => {
    if (mensaje === '') return
    const temporizador = setTimeout(() => onTerminar(''), 3000)
    // LIMPIEZA: cancela el temporizador si el componente se desmonta o cambia el mensaje.
    return () => clearTimeout(temporizador)
  }, [mensaje, onTerminar])

  if (mensaje === '') return null
  return <p className="aviso">{mensaje}</p>
}

export default Aviso
