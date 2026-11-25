# Exposición — Laboratorio 14: componentes de la aplicación de comercio electrónico (cafetería y Chamba PE)

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiante:** Renzo León
**Tema:** la estructura vacía del Lab 13 se llena con sus componentes: base de
datos (modelos y migraciones), rutas (router), controladores (ViewSets y
vistas con reglas), vistas (React) y un pago simulado. Parte 1 con el catálogo
de una **cafetería**; Parte 2 con la **solicitud de servicio de Chamba PE**.

> Regla clave: **el servidor decide el precio, el stock, el total y los estados.**

---

## El recorrido de una solicitud

```
Usuario → Vista de React (useEffect / botón) → Axios (api.js)
       → Ruta: config/urls.py → <app>/api_urls.py (DefaultRouter)
       → Controlador: ViewSet o @api_view  → Serializer (valida, arma JSON)
       → Modelo → ORM → SQLite → Response (JSON + código) → React redibuja
```

| Componente del sílabo | En el proyecto | Cafetería | Chamba PE |
|---|---|---|---|
| Base de datos | `models.py` + migraciones | [`catalogo/models.py`](../../django_project/src/catalogo/models.py), [`pedidos/models.py`](../../django_project/src/pedidos/models.py) | [`servicios`](../../django_project/src/servicios/models.py), [`clientes`](../../django_project/src/clientes/models.py), [`solicitudes`](../../django_project/src/solicitudes/models.py) |
| Rutas | `DefaultRouter` | [`catalogo/api_urls.py`](../../django_project/src/catalogo/api_urls.py), [`pedidos/api_urls.py`](../../django_project/src/pedidos/api_urls.py) | [`solicitudes/api_urls.py`](../../django_project/src/solicitudes/api_urls.py) |
| Controladores | ViewSet / `@api_view` | `ProductoViewSet`, [`crear_pedido`, `confirmar_pago`](../../django_project/src/pedidos/api_views.py) | [`SolicitudViewSet`](../../django_project/src/solicitudes/api_views.py) + acción `avanzar` |
| Validación | Serializer | `validate_precio` | `validate_direccion` + `validate()` |
| Vistas | `src/pages` | [`ProductosPage`](../../frontend/src/pages/ProductosPage.jsx) | [`SolicitudesPage`](../../frontend/src/pages/SolicitudesPage.jsx), [`SolicitudDetallePage`](../../frontend/src/pages/SolicitudDetallePage.jsx) |
| Pago | Pasarela (S16) | `Pago` simulado → pedido PAG | Descrito en el [README](../../README.md#módulo-de-pago-de-chamba-pe-se-implementa-en-la-semana-16) |

**En Django el controlador se llama *view*** (patrón MVT); con una API, lo que
cumple el papel del *template* es el componente de React.

---

# PARTE 1 — Catálogo y pedidos de la cafetería

## Pasos 1 a 3 — Modelos, migraciones y shell (Ejercicios 1 a 3)

- `Categoria(nombre)` y `Producto(nombre, precio DecimalField, stock PositiveIntegerField, activo, categoria FK PROTECT)`.
- `makemigrations` + `migrate`; en el shell: 2 categorías (Bebidas, Postres) y 5 productos.
- `Producto.objects.all()` equivale a `SELECT ... FROM "catalogo_producto"`.

## Paso 4 — Relaciones y `on_delete` (Ejercicio 4)

| Relación | `on_delete` | Por qué |
|---|---|---|
| Producto → Categoria | PROTECT | No perder a qué categoría pertenece lo vendido |
| DetallePedido → Producto | PROTECT | Un producto vendido no se borra |
| DetallePedido → Pedido | CASCADE | Las líneas no existen sin su pedido |
| Pedido → Cliente | PROTECT | Conservar quién compró |

Prueba: borrar la categoría *Postres* (2 productos) → **`ProtectedError`**.

## Pasos 5 y 6 — Serializer, controlador y rutas (Ejercicios 5 y 6)

`ProductoSerializer` (con `categoria_nombre` y `validate_precio` > 0 → **400**)
y `ProductoViewSet` (solo activos, `select_related`, `SearchFilter`). El
router genera `GET/POST /api/productos/` y `GET/PUT/PATCH/DELETE /api/productos/<id>/`.

## Paso 7 — Vista de React (Ejercicio 7)

`ProductosPage` pide `/productos/` con `api.get` en un `useEffect([])`, muestra
Cargando, error y la tabla con `map()` y `key`. Network: **GET 200**.

## Paso 8 — Crear pedido y pago simulado (Ejercicio 8)

`crear_pedido`: dentro de **`transaction.atomic`**, por cada producto
`filter(stock__gte=cantidad).update(stock=F('stock') - cantidad)`; precio
**desde la BD**; total **en el servidor**.

| Prueba | Resultado |
|---|---|
| 2 Capuchinos + 1 Café americano | **201**, total S/ 24.50, stock 40 → 38 y 50 → 49 |
| 1 Capuchino + 99 Tortas | **400** "Stock insuficiente de Torta de chocolate.", **stock sin cambios** (se deshizo todo) |
| Pagar el pedido | **200**, `Pago` APROBADO y pedido **PAG** |
| Pagarlo otra vez | **400** "Solo se puede pagar un pedido Pendiente." |

**Pago real (S16):** React obtiene un **token** de la pasarela; Django cobra
con su clave secreta y guarda monto, método, referencia y estado. **Nunca** se
guarda número de tarjeta, CVV ni vencimiento.

---

# PARTE 2 — La solicitud de servicio de Chamba PE

## Paso 9 y 10 — Componentes y modelos (Ejercicios 9 y 10)

- `Rubro` (servicios), `Cliente` (clientes), `Prestador` (chamba, Lab 12).
- **`Solicitud` (principal):** FK `cliente`, `prestador`, `rubro` con **PROTECT**; `monto` Decimal; `estado` con choices.
- **`SeguimientoSolicitud` (detalle):** FK `solicitud` con **CASCADE**; un registro por cambio de estado.
- Datos de prueba: [`cargar_lab14.py`](../../django_project/src/cargar_lab14.py) → 5 rubros, 4 clientes, 3 solicitudes, 9 seguimientos.

## Paso 11 — Serializer, ViewSet y reglas (Ejercicio 11)

| Regla | Dónde | Prueba |
|---|---|---|
| Dirección de al menos 8 caracteres | `validate_direccion` | **400** |
| Solo prestador **Aprobado** | `validate()` | María (Pendiente) → **400** |
| Mismo rubro que el prestador | `validate()` | — |
| Prestador sin otro servicio en curso | `validate()` | Rosa (Confirmada) → **400** |
| Monto = tarifa guardada | `perform_create` en `atomic` | Se envió 1.00 → guardó **60.00** (**201**) |
| Estados en orden | acción `avanzar` | PEN → CON **200**; Pagada → **400** |

También: PATCH **200**, DELETE **204**, GET posterior **404**, `?search=rosa` y `?estado=PEN`.
Chamba PE no maneja stock: la regla equivalente a `F()` es que **un prestador
no atiende dos servicios a la vez**.

## Paso 12 — Listado y detalle en React (Ejercicio 12)

`SolicitudesPage`: GET con carga, error, búsqueda y filtro. **Ver** guarda el
id en estado local y muestra `SolicitudDetallePage` (equivale a
`/solicitudes/:id`), con el seguimiento y el botón **Avanzar estado**.

## Pasos 13 y 14 — Pago y publicación (Ejercicios 13 y 14)

El README describe el pago (se invoca al quedar **Finalizada**; token + monto en
céntimos + PEN; pasa a **Pagada**; nunca datos de tarjeta). `manage.py check`,
`npm run lint` y `npm run build` sin errores, sin 500 y sin `node_modules`/`dist`.

## Resumen para el checklist

| Criterio | Dónde |
|---|---|
| Modelos con `on_delete` justificado | Pasos 4 y 10 |
| Migraciones y datos de prueba | Pasos 3 y 10 |
| Serializer con regla y 400 | Paso 11 |
| ViewSet con CRUD y búsqueda | Paso 11 |
| Rutas con router bajo `/api/` | [`config/urls.py`](../../django_project/src/config/urls.py) |
| Listado con carga y error (GET 200) | Paso 12 |
| Pantalla de detalle | Paso 12 |
| Pago descrito en el README | Paso 13 |
| check, lint, build y repo publicado | Paso 14 |
