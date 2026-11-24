# Exposición — Laboratorio 13: diseño de una aplicación de comercio electrónico (cafetería y Chamba PE)

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiante:** Renzo León
**Tema:** antes de escribir más código se **diseña** la aplicación: tipo de
comercio, módulos, roles, requisitos, reglas de negocio, arquitectura,
estructura de carpetas y mapa de rutas. Se aplica primero a una **cafetería
en línea** (Parte 1) y después al proyecto integrador **Chamba PE** (Parte 2).
Los modelos y la API completos se escriben en la **Semana 14**.

> Regla de oro del laboratorio: **el navegador muestra; el servidor decide.**

---

## De dónde partimos

Hasta el Lab 12 se construyeron **piezas separadas**: modelos, una API,
componentes de React y la conexión con Axios. El Lab 13 las reúne en una
**aplicación de comercio electrónico** y obliga a pensar primero qué se va a
construir.

```
Labs 8–12:  modelo → API → componente → Axios        (piezas sueltas)
Lab 13:     tipo de comercio → módulos → requisitos → reglas → arquitectura
            → apps de Django + carpetas de React → mapa de rutas   (diseño)
Lab 14:     modelos y API de cada app                 (recién se programa)
```

## Arquitectura: cómo funciona y para qué sirve

**Idea central.** Una aplicación de e-commerce **no es una página
informativa**: registra clientes, stock, pedidos y pagos. Por eso cada capa
tiene un papel fijo:

```
React (tienda y panel) ──HTTP + JSON──▶ API REST (DRF) ──vistas──▶ Django (reglas) ──ORM──▶ SQLite
                                                                       ▲
                                              Pasarela de pago ── token o confirmación
```

| Capa | Para qué sirve | Dónde |
|---|---|---|
| **React** | Dibuja la tienda y el panel; guarda el **carrito temporal** | [`frontend/src/`](../../frontend/src/api.js) |
| **`api.js`** | Una sola instancia de Axios con la dirección del servidor | [`api.js`](../../frontend/src/api.js) |
| **API REST (DRF)** | Expone los datos en JSON en rutas `/api/...` | `api_urls.py` de cada app |
| **Django** | Aplica las **reglas de negocio**: precio, stock, estados | apps `catalogo`, `pedidos`, `servicios`, `clientes`, `solicitudes`, `chamba` |
| **Base de datos** | Guarda productos, pedidos, prestadores, solicitudes | `db.sqlite3` |
| **Pasarela de pago** | Cobra; al sistema solo le llega un **token o la confirmación** | servicio externo (S16) |

**Por qué se diseñó así:**

- **El precio y el stock se validan en Django**: el navegador está en manos del cliente y se puede manipular.
- **El dinero es `Decimal`**, no `float`, para no tener errores de redondeo.
- **No se recibe el número de tarjeta**: lo maneja la pasarela; filtrar la base de datos no expone tarjetas.
- **Carrito ≠ pedido**: el carrito es temporal (estado de React); el pedido es un registro con estado.
- **Una app por tema del negocio** y React separado en `components`, `pages` y `api.js`.

---

# PARTE 1 — Tienda en línea de la cafetería

## Paso 1 — Tipo de comercio y canales (Ejercicio 1)

| Tipo | Quién vende a quién | Ejemplo peruano |
|---|---|---|
| B2C | Empresa → consumidor final | Inkafarma (tienda en línea) |
| B2B | Empresa → empresa | Makro (vende al por mayor a bodegas y restaurantes) |
| C2C | Persona → persona, con una plataforma | Neoauto (autos usados entre particulares) |

La cafetería es **B2C**. Los canales que usarían la **misma API**: web en
React, app móvil y redes sociales (catálogo de Instagram o WhatsApp con enlace
de pago). **M-commerce y social commerce son canales**, no tipos: dicen *por
dónde* se compra, no *quién le vende a quién*.

## Paso 2 — Módulos y roles (Ejercicio 2)

| Módulo | Semana | Módulo | Semana | Módulo | Semana |
|---|---|---|---|---|---|
| Catálogo | S14 | Carrito | S14 | Usuarios y roles | S15 |
| Pedidos | S14 | Pagos | **S16** | Inventario | S14 |
| Panel administrativo | S14 | Seguridad | S15 | Notificaciones | S14 |

| Rol | Qué puede hacer | Pantalla |
|---|---|---|
| Visitante | Ver el catálogo | Catálogo |
| Cliente | Carrito, pedidos, pagar, ver sus pedidos | Catálogo, carrito, mis pedidos |
| Administrador | Productos, stock y estados de pedido | Panel administrativo |

## Paso 3 — Requisitos (Ejercicio 3)

Cinco funcionales (RF01 catálogo, RF02 carrito, RF03 pedido, RF04 pago, RF05
gestión) y cinco no funcionales (seguridad, integridad del stock, usabilidad
en celular, rendimiento, disponibilidad), cada uno con **criterio de
aceptación**.

- **Funcional:** *qué* hace el sistema. **No funcional:** *qué tan bien* lo hace.
- Vago: *"El sistema debe ser rápido y seguro"* → no se puede comprobar.
- Verificables: **el catálogo carga en menos de 3 segundos** y **las contraseñas se guardan cifradas y todo va por HTTPS**.

## Paso 4 — Arquitectura y flujo de compra (Ejercicio 4)

| # | Paso | React | Django | Estado |
|---|---|---|---|---|
| 1 | Explorar | `GET /api/productos/` | Devuelve precio y stock | — |
| 2 | Carrito | Guarda en su estado | No interviene | — |
| 3 | Crear pedido | `POST /api/pedidos/` | Lee precio y stock **de la BD**, crea el pedido, baja el stock | **PEN** |
| 4 | Pagar | Lleva a la pasarela | Espera la confirmación | PEN |
| 5 | Confirmar | Muestra el pedido pagado | Recibe token o confirmación | **PAG** |
| 6 | Entrega | Muestra entregado | El administrador cambia el estado | **ENT** |

## Paso 5 — Reglas de negocio y errores comunes (Ejercicio 5)

| Regla | Dónde | Error que evita |
|---|---|---|
| Precio desde la base de datos | Django | Pagar menos cambiando el precio en el navegador |
| Validar y descontar el stock al crear el pedido | Django | Vender la última unidad a dos clientes |
| Dinero en `Decimal` | Django | Redondeos en totales |
| Solo token o confirmación, nunca la tarjeta | Django + pasarela | Robo de tarjetas |
| Carrito temporal, pedido con estado | React / Django | Tomar como venta algo no confirmado |

**Por qué el stock no puede vivir solo en React:** cada cliente tiene su
propia copia en el navegador; si dos compran la última unidad a la vez, las
dos pantallas creen que hay stock. Solo el servidor ve el stock real.

## Paso 6 — Apps de Django (Ejercicio 6)

`python manage.py startapp catalogo` y `startapp pedidos`, registradas en
[`INSTALLED_APPS`](../../django_project/src/config/settings.py). `python manage.py check` → **System check identified no
issues**. **Proyecto** = el sistema completo y su configuración (`config/`);
**app** = un módulo de un tema, reutilizable.

## Paso 7 — Estructura de React (Ejercicio 7)

`frontend/src/components/ProductoCard.jsx` y `frontend/src/pages/ProductosPage.jsx`
(vacíos) y [`api.js`](../../frontend/src/api.js) con `baseURL: 'http://127.0.0.1:8000/api'`.
**components** = piezas reutilizables; **pages** = pantallas completas, una
por ruta; **api.js** = la dirección del servidor en un solo lugar.

## Paso 8 — Mapa de rutas (Ejercicio 8)

| Recurso | API de Django | React |
|---|---|---|
| Productos | `/api/productos/` | `/productos` |
| Detalle | `/api/productos/<id>/` | `/productos/:id` |
| Categorías | `/api/categorias/` | `/productos?categoria=` |
| Carrito | sin API (estado de React) | `/carrito` |
| Pedidos | `/api/pedidos/` | `/pedidos` |

`runserver` arranca sin problemas y `npm run build` compila. **Ruta de la
API** = devuelve JSON y la usa el programa (Axios). **Ruta de React** = la ve
la persona y decide qué pantalla se dibuja.

---

# PARTE 2 — Proyecto integrador Chamba PE

## Paso 9 — Entidad y módulos (Ejercicio 9)

| Concepto | Chamba PE |
|---|---|
| Tipo de comercio | **C2C mediado por plataforma**: el prestador independiente le vende su servicio a una persona; Chamba PE pone la plataforma, la verificación y el cobro, y gana una comisión |
| Entidad principal | **Solicitud** de servicio (detalle: **SeguimientoSolicitud**) |
| Roles | Visitante, cliente, prestador, administrador |
| Dos reglas | Solo un prestador **Aprobado** recibe solicitudes · tarifa **> 0** en `Decimal` |
| Rutas | `/api/solicitudes/` ↔ `/solicitudes` · `/api/chamba/prestadores/` ↔ `/admin/prestadores` |

## Paso 10 — Módulos, requisitos y reglas (Ejercicio 10)

- **Ya construido:** prestadores y su panel (Labs 11 y 12, app `chamba`) y la búsqueda cercana y el inicio de sesión con roles (repo del equipo).
- **S14:** rubros, solicitudes, clientes, notificaciones · **S15:** roles, calificaciones · **S16:** pagos.
- 6 requisitos funcionales, 3 no funcionales y 5 reglas (ver el [README](../../README.md#parte-2--proyecto-integrador-chamba-pe)).

| Regla | Dónde |
|---|---|
| Solo prestadores Aprobados reciben solicitudes | Django |
| Tarifa > 0 y en `Decimal` | Django (aviso previo en React) |
| El monto sale de la tarifa guardada, no del navegador | Django |
| Un prestador no tiene dos servicios En servicio a la vez | Django |
| Estados en orden; solo se califica una solicitud Finalizada | Django (React solo muestra los botones posibles) |

## Paso 11 — Arquitectura y flujo principal (Ejercicio 11)

**Solicitar un servicio:** Buscar (`GET /api/chamba/prestadores/?rubro=&estado=Aprobado`)
→ Solicitar (`POST /api/solicitudes/`, **Pendiente**) → el prestador Acepta
(**Confirmada**) → **En camino** → **En servicio** → **Finalizada** → Pagar
(pasarela, **Pagada**) → Calificar.

Entidades para la Semana 14: `Rubro`, `Prestador`, `Cliente`, **`Solicitud`
(principal)**, **`SeguimientoSolicitud` (detalle)**, `Pago`, `Calificacion`.

## Paso 12 — Apps de Django (Ejercicio 12)

Nuevas: **`servicios`** (rubros), **`clientes`** y **`solicitudes`**; los
prestadores siguen en **`chamba`** desde el Lab 12. Registradas en
[`settings.py`](../../django_project/src/config/settings.py) y `manage.py check` sin errores. El proyecto **no tiene app
`core`**: la base es `config/`.

## Paso 13 — React y mapa de rutas (Ejercicio 13)

Páginas vacías en `src/pages/`: `RubrosPage`, `PrestadoresPage`,
`ClientesPage`, `SolicitudesPage`. `components` y `api.js` ya existían.

| Recurso | API de Django | React |
|---|---|---|
| Rubros | `/api/servicios/rubros/` | `/servicios` |
| Prestadores | `/api/chamba/prestadores/` | `/admin/prestadores` |
| Clientes | `/api/clientes/` | `/admin/clientes` |
| Solicitudes | `/api/solicitudes/` | `/solicitudes` |
| Detalle | `/api/solicitudes/<id>/` | `/solicitudes/:id` |
| Calificación | `/api/solicitudes/<id>/calificacion/` | `/solicitudes/:id/calificar` |

## Paso 14 — Verificar y publicar (Ejercicio 14)

`manage.py check`, `npm run lint` y `npm run build` sin errores;
`node_modules` y `dist` ignorados. El diseño completo de las dos partes está
en el [README](../../README.md) de la raíz.

## Resumen para el checklist

| Criterio | Dónde |
|---|---|
| Tipo de comercio, canales y roles | Pasos 9 y 10 |
| Mapa de módulos con lo ya construido | Paso 10 |
| Requisitos funcionales y no funcionales verificables | [README](../../README.md) |
| Reglas de negocio y dónde se aplican | Paso 10 |
| Arquitectura, flujo y entidades | Paso 11 |
| Apps creadas y registradas; `check` sin errores | Paso 12 |
| `components`, `pages` y `api.js` | Paso 13 |
| Mapa de rutas | Paso 13 |
| Lint, build y README con el diseño | Paso 14 |
