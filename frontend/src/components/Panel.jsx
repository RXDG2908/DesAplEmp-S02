// ==================================================================
// GUIA: ARCHIVO  components/Panel.jsx
// LAB     : 10 (children)  -  PARTE 2 (biblioteca)
// QUE HACE : contenedor con titulo para las secciones de la biblioteca (equivale a ./Tarjeta.jsx de vet). Usado en ../App.jsx.
// ==================================================================
function Panel({ titulo, children }) {
  return (
    <section className="panel">
      <h2>{titulo}</h2>
      {children}
    </section>
  )
}

export default Panel