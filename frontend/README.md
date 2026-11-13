# Frontend (React + Vite)

Interfaz del Laboratorio 9 con datos escritos a mano, con la forma de la API
REST de la Semana 8. Todavía no consume la API.

## Qué muestra

- `src/Vet.jsx` — veterinaria, armada con componentes y datos de
  `src/datos.js`.
- `src/components/` — `InsumoCard` (botón Reservar con `useState`),
  `InsumoLista` (búsqueda controlada y formulario con validación de stock),
  `CitaCard` (cita con sus consumos), `ConsumoItem` (un consumo) y `Tarjeta`
  (contenedor con `children`).
- Inicio (`src/App.jsx`) — biblioteca: categorías, libros y socios con sus
  préstamos y multas. Importa y muestra `Vet`.
- `src/practica/` — Laboratorio 11, Parte 1: mini catálogo de cafetería con
  carrito. `Practica` (padre con el estado), `Catalogo`, `ProductoCard`,
  `Carrito` (total y unidades calculados), `Buscador` y `Aviso`.
- `src/components/PanelCitas.jsx` — Laboratorio 11, Parte 2: panel de citas.
  El padre guarda las citas y reparte a `CitaListado`/`CitaFila` (Confirmar y
  Eliminar), `CitaForm` (alta con validación), `ResumenCitas`, `BuscadorCitas`
  y `Aviso`.
- `src/App.jsx` — botones para ver Inicio, la práctica de cafetería o el panel de
  citas.
- `src/components/PanelPrestadores.jsx` — Laboratorio 11, Parte 2: panel
  administrativo del proyecto integrador Chamba PE. El padre guarda los
  prestadores (`src/datosChamba.js`) y reparte a `PrestadorListado`/
  `PrestadorFila` (Aprobar, Suspender y Eliminar), `PrestadorForm` (alta con
  validación de nombres y tarifa mayor que cero), `ResumenPrestadores` (conteo
  por estado y tarifa promedio), `BuscadorPrestadores` y `Aviso`.
- `src/App.css` — estilos de ambas secciones.

## Cómo ejecutarlo

```bash
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173/. Otros scripts: `npm run lint` y `npm run build`.
`node_modules` y `dist` no se suben al repositorio.

## Pendiente

Los datos siguen escritos a mano; falta consumir la API de Django con `fetch`.
