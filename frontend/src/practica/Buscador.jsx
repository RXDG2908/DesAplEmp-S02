// ==================================================================
// ARCHIVO  : practica/Buscador.jsx
// PARTE 1  : práctica del Lab 11 (mini catálogo con carrito: CAFETERÍA)
// ------------------------------------------------------------------
// LAB 11 - EJ 7: CAMPO CONTROLADO; el VALOR vive en el padre y cada cambio se
//                AVISA con onCambiar. Buscador y Catalogo son HERMANOS: no se
//                hablan directamente, se comunican A TRAVÉS DEL PADRE.
// ------------------------------------------------------------------
// USADO EN : ./Practica.jsx
// ------------------------------------------------------------------
// DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
//   LAB 11 - EJ 7 .... línea 16
// ==================================================================
function Buscador({ valor, onCambiar }) {
  return (
    <input
      type="text"
      placeholder="Buscar producto"
      value={valor}
      onChange={(e) => onCambiar(e.target.value)}
    />
  )
}

export default Buscador
