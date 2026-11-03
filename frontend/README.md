# Frontend (React + Vite)

Interfaz del Laboratorio 9 con datos escritos a mano, con la forma de la API
REST de la Semana 8. Todavía no consume la API.

## Qué muestra

- `src/Vet.jsx` — veterinaria: lista de insumos (con "Sin stock" y "¡Última
  unidad!"), citas con ficha clínica opcional y lista anidada de consumos con
  total por cita.
- `src/App.jsx` — biblioteca: categorías, libros y socios con sus préstamos y
  multas. Importa y muestra `Vet`.
- `src/App.css` — estilos de ambas secciones.

## Cómo ejecutarlo

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173/. Otros scripts: `npm run lint` y `npm run build`.
`node_modules` y `dist` no se suben al repositorio.
