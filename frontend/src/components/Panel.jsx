function Panel({ titulo, children }) {
  return (
    <section className="panel">
      <h2>{titulo}</h2>
      {children}
    </section>
  )
}

export default Panel