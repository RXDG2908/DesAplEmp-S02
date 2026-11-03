# Exposición — Laboratorio 09, Parte 1: interfaz React para la veterinaria (`vet`)

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** construir con React (Vite) una interfaz para la app `vet`, con datos
escritos a mano que tienen la forma de la API REST de la Semana 8.

> Explica en orden lo hecho en la Parte 1 del Laboratorio 9. La Parte 2 (la
> biblioteca) está en `App.jsx`; la veterinaria está en `Vet.jsx`.

---

## De dónde partimos

En el Laboratorio 8 la app `vet` quedó expuesta como API: `/api/insumos/` y
`/api/citas/` devuelven JSON. Una cita trae su veterinario (1:N), su ficha
clínica (1:1, puede ser `null`) y sus consumos (N:M con `ConsumoInsumo`).
En este laboratorio todavía **no se consume la API** (eso es la Semana 12):
los datos se escriben a mano, pero con la misma forma que el JSON real, por
ejemplo `stock: 100` y los decimales como texto (`precio_unitario: "1.50"`).

```
Navegador (localhost:5173) → main.jsx → App.jsx → Vet.jsx → JSX → pantalla
```

## Paso 1 — Entorno: Node.js y npm (Ejercicio 1)

Se instaló Node.js LTS (`node -v` → v26.13.0, `npm -v` → 11.20.0).

| Elemento | Python / Django | Node.js / React |
|---|---|---|
| Lenguaje | Python | JavaScript (JSX) |
| Gestor de paquetes | pip | npm |
| Archivo de dependencias | `requirements.txt` | `package.json` |
| Carpeta de dependencias | `venv/Lib/site-packages` | `node_modules` |
| Comando del servidor de desarrollo | `python manage.py runserver` | `npm run dev` |

## Paso 2 — Crear el proyecto con Vite (Ejercicio 2)

`npm create vite@latest frontend -- --template react`, luego `npm install` y
`npm run dev`. El servidor queda en http://localhost:5173/. La carpeta
`frontend` vive dentro del repositorio, junto a `django_project`.

## Paso 3 — Estructura del proyecto (Ejercicio 3)

| Archivo | Papel | Equivalente en Django |
|---|---|---|
| `index.html` | Única página; tiene el `<div id="root">` | `base.html` |
| `main.jsx` | Arranca React y monta `<App />` en `#root` | `manage.py` / `wsgi.py` (punto de entrada) |
| `App.jsx` | Componente principal con el JSX | Template + View juntos |
| `package.json` | Dependencias y scripts (`dev`, `build`, `lint`) | `requirements.txt` |
| `node_modules` | Paquetes instalados (no se sube a Git) | `venv` |

## Paso 4 — Primer JSX con expresiones (Ejercicio 4)

En `Vet.jsx`, el componente `Vet` muestra el título en un `<h1>` y usa llaves:
`{aplicacion}` (una variable) y
`{(precioConsulta * (1 + igv)).toFixed(2)}` (un cálculo). Con consulta de
S/ 40.00 e IGV 18 % muestra S/ 47.20.

## Paso 5 — Lista con `map()` y `key` (Ejercicio 5)

El arreglo `insumos` tiene cinco registros con la forma de `/api/insumos/`
(`id`, `nombre`, `unidad`, `stock`). Se muestran con
`insumos.map((insumo) => <li key={insumo.id}>…)`. La `key` le permite a React
identificar cada elemento cuando la lista cambia. **Equivale al
`{% for insumo in insumos %}` de los Templates de Django.** Las citas también
usan `key={cita.id}` y se convierten los decimales con
`Number(...).toFixed(2)`.

## Paso 6 — Renderizado condicional (Ejercicio 6)

- Ternario: `insumo.stock === 0 ? <span className="sin-stock">Sin stock</span> : \`Stock: ${insumo.stock}\``.
- `&&`: `insumo.stock === 1 && <strong> ¡Última unidad!</strong>`.
- Lista vacía: `insumos.length === 0 ? <p>No hay registros</p> : …`. Se probó
  vaciando temporalmente el arreglo (`const insumos = []`) y aparece el
  mensaje.
- En la cita: `cita.ficha ? …ficha… : <p>Sin ficha clínica</p>` (la ficha 1:1
  puede ser `null`) y `Por confirmar` solo si el estado es `Pendiente`.

## Paso 7 — Relación anidada (Ejercicio 7)

Cada cita (`citas.map`) contiene sus consumos (`cita.consumos.map`), cada uno
con su propia `key`. Por cita se calcula el total con
`consumos.reduce((suma, c) => suma + Number(c.subtotal), 0).toFixed(2)`.
Ejemplo: Firulais → 1.50 + 25.00 = S/ 26.50; Rocky → 16.00 + 7.50 = S/ 23.50.
Las citas sin consumos muestran "Sin consumos" y total S/ 0.00.

## Paso 8 — Estilos y verificación (Ejercicio 8)

- Clases en `App.css`: `.seccion-vet`, `.sin-stock`, `.tarjeta-cita`.
- Estilo en línea: `<h2 style={{ color: '#1f5f5b' }}>`.
- Al cambiar un dato (por ejemplo un `stock`) Vite recarga y la pantalla se
  actualiza sola (HMR).
- `npm run lint` → sin errores. `npm run build` → "✓ built", 18 módulos.

**Diferencia con los Templates de la Semana 6:** el Template se arma en el
servidor y el navegador recibe HTML terminado; en React el navegador descarga
JavaScript y construye la interfaz allí. **Falta** consumir la API de la
Semana 8 con `fetch` (Semana 12), resolver CORS entre `localhost:5173` y
Django, y reemplazar los arreglos escritos a mano por la respuesta real.

## Resumen para el checklist

| Criterio | Dónde |
|---|---|
| Node y npm | Paso 1 |
| Vite en `frontend`, puerto 5173 | Paso 2 |
| JSX con título y 2 expresiones | `Vet.jsx`, Paso 4 |
| Dos listas con `map()` y `key` | insumos y citas |
| Condicional y lista vacía | Paso 6 |
| Relación anidada | Paso 7 |
| Estilos con `className` y CSS | `App.css` |
| Lint y build sin errores | Paso 8 |
