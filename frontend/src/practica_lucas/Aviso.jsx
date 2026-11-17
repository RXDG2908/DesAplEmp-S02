import { useEffect, useState } from 'react'

function Aviso({ nombre }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const temporizador = setTimeout(() => setVisible(false), 3000)
    return () => clearTimeout(temporizador)
  }, [])

  if (!visible) {
    return null
  }

  return <p className="aviso-cafe">Agregado: {nombre}</p>
}

export default Aviso
