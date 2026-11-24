# DesAplEmp-S02 — Desarrollo de Aplicaciones Empresariales

Repositorio del curso (4 - C24 - Sección CD). Proyecto Django en
`django_project/src/` y frontend React + Vite en `frontend/`.

- Cómo ejecutar el frontend y la API: ver [frontend/README.md](frontend/README.md).
- Índice por semana: [INDICE_SEMANAS.md](INDICE_SEMANAS.md).
- Exposiciones y guiones de cada laboratorio: [docs/exposiciones/](docs/exposiciones/) y [docs/guiones/](docs/guiones/) (Lab 13: [exposición](docs/exposiciones/EXPOSICION_Lab13.md) y [guion](docs/guiones/GUION-Lab13.md)).

---

## Laboratorio 13 — Diseño de una aplicación de comercio electrónico

Antes de escribir los modelos (Semana 14) se define qué hace la aplicación,
sus reglas, su arquitectura y su estructura de carpetas y rutas.

### Parte 1 — Tienda en línea de la cafetería

**Tipo de comercio:** B2C (la cafetería vende al consumidor final). Canales que
usan la misma API de Django: la web en React, una app móvil y las redes sociales
(catálogo de Instagram o WhatsApp con enlace de pago).

**Módulos y semana en que se implementan**

| Módulo | Semana |
|---|---|
| Catálogo de productos (precio, categoría y stock) | S14 |
| Carrito de compras | S14 |
| Usuarios y roles | S15 |
| Gestión de pedidos | S14 |
| Pagos en línea (pasarela) | S16 |
| Inventario | S14 |
| Panel administrativo | S14 |
| Seguridad | S15 |
| Notificaciones y reportes | S14 |

**Roles:** visitante (ve el catálogo), cliente (compra y ve sus pedidos) y
administrador (gestiona productos y estados de pedido desde el panel).

**Reglas de negocio**

| Regla | Dónde | Error que evita |
|---|---|---|
| El precio se lee de la base de datos, no del navegador | Django | Que alguien cambie el precio en el navegador y pague menos |
| No se vende más que el stock; se valida y se descuenta al crear el pedido | Django | Vender la última unidad a dos clientes |
| El dinero se guarda con `DecimalField` / `Decimal`, nunca `float` | Django | Errores de redondeo en totales |
| El sistema no recibe ni guarda el número de tarjeta; solo el token o la confirmación de la pasarela | Django + pasarela | Robo de datos de tarjeta |
| El carrito es temporal (estado de React); el pedido es un registro con estado | React (carrito) y Django (pedido) | Tratar como venta algo que el cliente aún no confirmó |

**Apps de Django:** `catalogo` (productos y categorías) y `pedidos` (pedidos y
su detalle). **React:** `src/components/ProductoCard.jsx`,
`src/pages/ProductosPage.jsx` y `src/api.js` (instancia de Axios).

**Mapa de rutas**

| Recurso | API de Django | Ruta de React |
|---|---|---|
| Productos | `/api/productos/` | `/productos` |
| Detalle de producto | `/api/productos/<id>/` | `/productos/:id` |
| Categorías | `/api/categorias/` | `/productos?categoria=` |
| Carrito | (sin API: estado de React) | `/carrito` |
| Pedidos | `/api/pedidos/` | `/pedidos` |
| Detalle de pedido | `/api/pedidos/<id>/` | `/pedidos/:id` |

### Parte 2 — Proyecto integrador Chamba PE

Chamba PE conecta a clientes con prestadores verificados (gasfiteros,
electricistas, costureros, primeros auxilios) que están cerca y disponibles
ahora, al estilo de un delivery.

**Tipo de comercio:** C2C mediado por una plataforma: un prestador
independiente le vende un servicio a una persona y Chamba PE pone la
plataforma, la verificación y el cobro (cobra una comisión). Canales: web en
React, app móvil y redes sociales para captar prestadores.

**Módulos**

| Módulo | Estado |
|---|---|
| Catálogo de rubros y servicios | S14 (app `servicios`) |
| Prestadores y su verificación (panel de revisión) | Construido en los Labs 11 y 12 (app `chamba`) |
| Búsqueda de prestadores cercanos | Construida en el repo del equipo (Sprint 1) |
| Usuarios y roles | S15 (el repo del equipo ya tiene inicio de sesión con roles) |
| Solicitudes de servicio y su seguimiento | S14 (app `solicitudes`) |
| Clientes | S14 (app `clientes`) |
| Pagos | S16 |
| Calificaciones y reseñas | S15 |
| Panel administrativo | Construido en los Labs 11 y 12 (prestadores) |
| Notificaciones al prestador | S14 |

**Roles**

| Rol | Qué puede hacer | Pantalla |
|---|---|---|
| Visitante | Ver rubros y buscar prestadores | `/servicios`, `/prestadores` |
| Cliente | Pedir un servicio, seguirlo, pagar y calificar | `/solicitudes`, `/solicitudes/:id` |
| Prestador | Aceptar solicitudes y cambiar su estado | `/mis-solicitudes` |
| Administrador | Aprobar o suspender prestadores y revisar solicitudes | `/admin/prestadores`, `/admin/solicitudes` |

**Requisitos funcionales**

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF01 | El cliente verá los prestadores aprobados de un rubro | Alta | La lista solo muestra prestadores con estado Aprobado |
| RF02 | El cliente podrá crear una solicitud de servicio | Alta | Al enviarla queda en estado Pendiente con fecha y prestador |
| RF03 | El prestador podrá aceptar o rechazar una solicitud | Alta | Al aceptar pasa a Confirmada; al rechazar, a Rechazada |
| RF04 | El cliente podrá seguir el estado de su solicitud | Media | Ve Confirmada, En camino, En servicio y Finalizada en orden |
| RF05 | El administrador podrá aprobar o suspender prestadores | Alta | Un prestador suspendido deja de aparecer en la búsqueda |
| RF06 | El cliente podrá calificar el servicio al terminar | Media | Solo puede calificar una vez y solo si está Finalizada |

**Requisitos no funcionales**

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RNF01 | Seguridad: contraseñas cifradas y HTTPS | Alta | En la base de datos no aparece ninguna contraseña en texto plano |
| RNF02 | Rendimiento: la búsqueda responde rápido | Alta | La lista de prestadores carga en menos de 3 segundos |
| RNF03 | Usabilidad: funciona en el celular | Media | La pantalla de solicitud se ve completa en un ancho de 375 px |

**Reglas de negocio**

| Regla | Dónde | Error que evita |
|---|---|---|
| Solo un prestador Aprobado puede recibir solicitudes | Django | Mandar a un desconocido sin verificar a la casa del cliente |
| La tarifa es mayor que cero y se guarda como `Decimal` | Django (y aviso en React) | Servicios gratis por error o totales mal redondeados |
| El precio de la solicitud se toma de la tarifa guardada, no del navegador | Django | Que el cliente cambie el monto antes de pagar |
| Un prestador no puede tener dos servicios En servicio a la vez | Django | Prometer dos visitas a la misma hora |
| Los estados avanzan en orden y solo se califica una solicitud Finalizada | Django (React solo muestra los botones posibles) | Calificar o cobrar un servicio que no se hizo |

**Entidades para la Semana 14:** `Rubro`, `Prestador`, `Cliente`,
**`Solicitud` (entidad principal)**, **`SeguimientoSolicitud` (detalle: cada
cambio de estado)**, `Pago` y `Calificacion`.

**Arquitectura y flujo de una solicitud**

```
React (tienda y panel) --HTTP + JSON--> API REST (DRF) --> Django (reglas) --ORM--> SQLite
                                                              |
                                                     Pasarela de pago (token / confirmación)

1. Buscar       GET  /api/chamba/prestadores/?rubro=...&estado=Aprobado
2. Solicitar    POST /api/solicitudes/          -> Pendiente
3. Aceptar      PATCH /api/solicitudes/<id>/    -> Confirmada (prestador)
4. Ir y atender PATCH ...                       -> En camino -> En servicio
5. Terminar     PATCH ...                       -> Finalizada
6. Pagar        pasarela -> Django guarda la confirmación -> Pagada
7. Calificar    POST /api/solicitudes/<id>/calificacion/
```

**Apps de Django:** `servicios` (rubros), `chamba` (prestadores, desde el Lab
12), `clientes` y `solicitudes`. El proyecto no tiene una app `core`: la
configuración base está en `config/`.

**React:** `src/components/` (componentes del panel), `src/pages/`
(`RubrosPage.jsx`, `PrestadoresPage.jsx`, `ClientesPage.jsx`,
`SolicitudesPage.jsx`, vacías por ahora) y `src/api.js`.

**Mapa de rutas**

| Recurso | API de Django | Ruta de React |
|---|---|---|
| Rubros | `/api/servicios/rubros/` | `/servicios` |
| Prestadores | `/api/chamba/prestadores/` | `/admin/prestadores` |
| Clientes | `/api/clientes/` | `/admin/clientes` |
| Solicitudes | `/api/solicitudes/` | `/solicitudes` |
| Detalle de solicitud | `/api/solicitudes/<id>/` | `/solicitudes/:id` |
| Calificación | `/api/solicitudes/<id>/calificacion/` | `/solicitudes/:id/calificar` |

### Pendiente

Semana 14: escribir los modelos y la API de `catalogo`, `pedidos`,
`servicios`, `clientes` y `solicitudes`, y llenar las páginas de React.
