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

## Laboratorio 12: React consume la API de Django

La dirección del servidor está solo en `src/api.js` (instancia de Axios).

- **Parte 1** — `src/practica/ListaPractica.jsx` (botón *Insumos desde la API*):
  lista, crea, cambia el stock y elimina insumos de `/api/insumos/`, con
  estados de carga, error y lista vacía, y búsqueda con `?search=`.
- **Parte 2** — `src/components/PanelPrestadores.jsx` (botón *Panel Chamba PE*):
  el panel de prestadores del proyecto integrador ya no usa datos a mano. Lista
  con GET, registra con POST, edita, aprueba y suspende con PATCH, y elimina con
  DELETE tras un segundo clic de confirmación (maneja 204 y 404). Busca por
  nombre y filtra por estado enviando parámetros a la API. El resumen se calcula
  con los datos recibidos.

### Ejecutar Django y React a la vez

```bash
# Terminal 1: Django (puerto 8000)
cd django_project/src
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < cargar_chamba.py   # prestadores de ejemplo
python manage.py runserver

# Terminal 2: React (puerto 5173)
cd frontend
npm install
npm run dev
```

### CORS

`django-cors-headers` está en `INSTALLED_APPS`, su middleware va al inicio de
`MIDDLEWARE` y `CORS_ALLOWED_ORIGINS` permite `http://localhost:5173`
(`config/settings.py`).

### Endpoints que usa el panel (app `chamba`)

- `GET /api/chamba/prestadores/` con `?search=` (nombres y apellidos),
  `?estado=` y `?ordering=`
- `POST /api/chamba/prestadores/` (400 si la tarifa no es mayor que cero)
- `PATCH /api/chamba/prestadores/<id>/` y `DELETE /api/chamba/prestadores/<id>/`

## Pendiente

La API sigue abierta a cualquier persona: faltan la autenticación y los permisos
(en Chamba PE el panel solo debería usarlo el administrador).
