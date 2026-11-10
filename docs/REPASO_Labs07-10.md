# Repaso rápido — Laboratorios 7, 8, 9 y 10 (Parte 1, app `vet`)

Una página para repasar antes de exponer. El detalle está en
`docs/guiones/` (para hablar) y `docs/exposiciones/` (completo).

## Antes de exponer: levantar la demo

```powershell
# Django (Labs 7 y 8) → http://localhost:8000/
cd django_project\src
..\venv\Scripts\python.exe manage.py runserver

# React (Labs 9 y 10) → http://localhost:5173/
cd frontend
npm run dev
```

Si es una PC nueva: `pip install -r requirements.txt`, `python manage.py migrate`
y, en `frontend`, `npm install`.

| Para mostrar | URL |
|---|---|
| Registrar consumo (Lab 7) | `/consumo/nuevo/` |
| Reporte (Lab 7) | `/reporte/` |
| Listado filtrado (Lab 7) | `/?estado=Pendiente` |
| Raíz de la API (Lab 8) | `/api/` |
| Insumos con búsqueda y orden (Lab 8) | `/api/insumos/?search=jer&ordering=-stock` |
| Citas por estado (Lab 8) | `/api/citas/?estado=Pendiente` |
| Acción propia (Lab 8) | `/api/citas/proximas/` |
| Interfaz React (Labs 9 y 10) | `http://localhost:5173/` |

---

## Lab 7 — ORM avanzado

**Idea en una frase:** usar el ORM más allá del CRUD, sin crear entidades nuevas.

| Concepto | Dónde | Qué decir |
|---|---|---|
| `transaction.atomic()` | `vet/views.py` → `consumo_registrar` | Crea el consumo, pone la cita Atendida y descuenta stock: o todo o nada |
| `F('stock') - cantidad` | misma vista | La resta la hace la base de datos; no se pierden descuentos simultáneos |
| `aggregate()` | `vet/views.py` → `reporte` | Un solo valor para toda la tabla → diccionario, no QuerySet |
| `annotate()` | misma vista | Un valor por objeto o grupo → sigue siendo QuerySet |
| `CitaQuerySet` | `vet/models.py` | `con_estado()` y `proximas()`, con `as_manager()`; reglas en un solo lugar |
| N+1 | `medir_n1.py` | `select_related` (de a uno, JOIN) y `prefetch_related` (de a muchos) |

**Números:** éxito 8→9 consumos y stock 100→98 · falla 9999: nada cambia ·
total S/ 110.50 · N+1: **6→1** y **15→3** consultas.

## Lab 8 — API REST con Django REST Framework

**Idea en una frase:** exponer las mismas citas e insumos como JSON, sin tocar `models.py`.

| Concepto | Dónde | Qué decir |
|---|---|---|
| Serializer | `vet/serializers.py` | Es el `Form` de la API: convierte a JSON y valida |
| `validate_stock` | `InsumoSerializer` | Regla de negocio: stock de al menos 1 |
| `many=True` | shell | Para serializar una colección y no un solo objeto |
| Anidados | `CitaSerializer` | Trae veterinario, ficha (puede ser `null`) y consumos |
| Vistas genéricas → ViewSet | `vet/api_views.py` | `ModelViewSet` reemplaza `ListCreate` + `RetrieveUpdateDestroy` |
| Router | `vet/api_urls.py` | `DefaultRouter` genera lista, detalle y la raíz `/api/` |
| Filtros | `InsumoViewSet` / `CitaViewSet` | `?search=`, `?ordering=`, `?estado=` con `con_estado()` |
| `@action(detail=False)` | `CitaViewSet.proximas` | Reutiliza `proximas()` del Lab 7 |

**Números:** códigos probados **200, 201, 400, 204, 404** · consultas de la API de citas **24→3**.
**Falta:** seguridad (la API está abierta).

## Lab 9 — Interfaz React con Vite

**Idea en una frase:** el navegador arma la pantalla con JavaScript (antes el servidor mandaba HTML).

| Concepto | Dónde | Qué decir |
|---|---|---|
| Node y npm | `package.json` | Equivalen a pip y `requirements.txt`; `node_modules` ≈ `venv` |
| Estructura | `index.html` → `main.jsx` → `App.jsx` → `Vet.jsx` | Un solo `div#root` donde React monta todo |
| JSX y `{ }` | `Vet.jsx` | Consulta con IGV: S/ 47.20 con `toFixed(2)` |
| `map()` + `key` | lista de insumos | Es el `{% for %}` de los Templates |
| Condicionales | ternario y `&&` | "Sin stock", "¡Última unidad!", "Sin ficha clínica" |
| Relación anidada | citas → consumos | `map` dentro de `map`; `reduce` suma: Firulais 26.50, Rocky 23.50 |

**Falta:** consumir la API con `fetch` y CORS (Semana 12).

## Lab 10 — Componentes, props, estado y eventos

**Idea en una frase:** dividir `Vet.jsx` en componentes reutilizables (como un `include` de Django).

| Concepto | Dónde | Qué decir |
|---|---|---|
| Componentes | `frontend/src/components/` | `InsumoCard`, `InsumoLista`, `CitaCard`, `ConsumoItem`, `Tarjeta`; nombre en mayúscula |
| Props | `InsumoCard` | Solo lectura; `unidad` con valor por defecto |
| `children` | `Tarjeta` | Lo que va entre sus etiquetas, como un `block` de Templates |
| `useState` + `onClick` | `InsumoCard` | Contador de reservados; React redibuja solo al cambiar el estado |
| Campo controlado | `InsumoLista` | `value` del estado + `onChange`; filtra sin distinguir mayúsculas |
| Formulario controlado | `InsumoLista` | `onSubmit` + `preventDefault`; stock ≥ 1; arreglo nuevo con spread |

**Falta:** guardar en la base de datos (hoy el insumo nuevo se pierde al recargar).

---

## El hilo que une los cuatro labs

Lab 7 crea `con_estado()` y `proximas()` → el Lab 8 los reutiliza en la API
→ los Labs 9 y 10 muestran los mismos datos (con la forma del JSON del Lab 8)
en React → en la Semana 12 React consumirá esa API con `fetch`.

## Preguntas probables

| Pregunta | Respuesta corta |
|---|---|
| ¿Por qué `aggregate()` no devuelve QuerySet? | Resume todo en un valor; no es una colección de objetos |
| ¿`select_related` o `prefetch_related`? | De a uno (FK, 1:1) → select; de a muchos (M2M, inversa) → prefetch |
| ¿Qué pasa si falla la transacción? | Se deshace todo, también lo que ya se había guardado dentro del bloque |
| ¿Para qué `F()`? | Para que la base de datos haga la resta y no se pierdan cambios simultáneos |
| ¿Serializer vs Form? | Mismo papel: convertir y validar; el serializer responde JSON |
| ¿Qué te da el router? | Las rutas de lista y detalle con todos los métodos HTTP, sin escribirlas |
| ¿Por qué `key` en `map()`? | Para que React sepa qué elemento cambió |
| ¿Por qué `useState` y no una variable? | React solo vuelve a dibujar cuando cambia el estado |
| ¿Props o estado? | Props vienen del padre y no se modifican; el estado es propio y cambia |
