# Guión expositivo — Laboratorio 13 (Diseño de la cafetería en línea y de Chamba PE)

## Introducción

"Hasta el laboratorio anterior construimos piezas sueltas: modelos, una API,
componentes de React y la conexión con Axios. En este laboratorio esas piezas
se juntan en una aplicación de comercio electrónico, pero todavía no
programamos los modelos: primero la diseñamos. Definimos el tipo de comercio,
los módulos, los roles, los requisitos, las reglas de negocio, la arquitectura
y la estructura de carpetas y rutas. Lo hago primero con una cafetería en
línea y después con mi proyecto integrador, Chamba PE. Los modelos y la API se
escriben en la Semana 14."

## Arquitectura: cómo funciona y para qué sirve

"Una aplicación de comercio electrónico no es una página que solo informa:
registra clientes, stock, pedidos y pagos. Por eso cada capa tiene un papel.
React dibuja la tienda y el panel, y guarda el carrito mientras el cliente
elige. Axios, desde [`api.js`](../../frontend/src/api.js), lleva las peticiones a la API. La API de Django
devuelve JSON. Django aplica las reglas y guarda con el ORM en la base de
datos. Y la pasarela de pago, que es un servicio externo, cobra y solo nos
devuelve un token o la confirmación.

La regla de oro es: el navegador muestra y el servidor decide. Por eso el
precio y el stock se validan en Django, no en React. Lo explico con un caso:
si dos clientes compran la última unidad al mismo tiempo, las dos pantallas
creen que hay stock, porque cada una tiene su copia. Solo el servidor ve el
stock real y puede aceptar un pedido y rechazar el otro."

## 1. Tipo de comercio y canales

"La cafetería es B2C, porque le vende directo al consumidor. B2B es de empresa
a empresa, como Makro, que vende al por mayor a bodegas. C2C es entre
personas con una plataforma de por medio, como Neoauto con los autos usados.
La misma API la pueden usar la web, una app móvil y las redes sociales. El
m-commerce y el social commerce no son tipos de comercio: dicen por dónde se
compra, no quién le vende a quién."

## 2. Módulos, roles y requisitos

"La tienda tiene nueve módulos. En la Semana 14 van el catálogo, el carrito,
los pedidos, el inventario, el panel y las notificaciones; en la 15, los
usuarios y la seguridad; y en la 16, los pagos. Hay tres roles: el visitante
mira el catálogo, el cliente compra y ve sus pedidos, y el administrador
gestiona productos y estados.

Los requisitos funcionales dicen qué hace el sistema, y los no funcionales qué
tan bien lo hace. 'Debe ser rápido y seguro' no se puede comprobar; lo
convertí en dos requisitos medibles: el catálogo carga en menos de tres
segundos y las contraseñas se guardan cifradas."

## 3. Flujo de compra y reglas

"El flujo es: explorar el catálogo, armar el carrito en React, crear el pedido
con un POST, donde Django lee el precio y el stock de la base de datos y deja
el pedido Pendiente, pagar en la pasarela, confirmar y entregar.

Las reglas son cinco: el precio se lee de la base de datos y no del
navegador; el stock se valida y se descuenta en el servidor; el dinero se
guarda como Decimal y no como float; nunca recibimos el número de tarjeta,
solo la confirmación de la pasarela; y el carrito es temporal mientras que el
pedido es un registro con estado."

## 4. Apps, carpetas y rutas de la cafetería

"Con startapp creamos las apps catalogo y pedidos y las registramos en
[`settings.py`](../../django_project/src/config/settings.py); `manage.py check` no muestra errores. Un proyecto es el sistema
completo con su configuración; una app es un módulo de un solo tema. En React
separamos components, que son piezas reutilizables, de pages, que son
pantallas completas. El mapa de rutas une cada recurso: por ejemplo,
`/api/productos/` es lo que pide el programa y `/productos` es lo que ve la
persona en el navegador."

## 5. Chamba PE: tipo, entidad y reglas

"Chamba PE es C2C mediado por una plataforma: un prestador independiente le
vende su servicio a una persona, y Chamba PE pone la plataforma, la
verificación y el cobro a cambio de una comisión. Hay cuatro roles: visitante,
cliente, prestador y administrador.

La entidad principal es la solicitud de servicio, y su detalle es el
seguimiento de cada cambio de estado. Las reglas más importantes: solo un
prestador aprobado puede recibir solicitudes, la tarifa debe ser mayor que
cero y se guarda como Decimal, el monto se toma de la tarifa guardada y no del
navegador, un prestador no puede atender dos servicios a la vez, y los estados
avanzan en orden; solo se califica una solicitud finalizada."

## 6. Flujo principal y estructura de Chamba PE

"El flujo es: el cliente busca prestadores aprobados del rubro, envía la
solicitud, que queda Pendiente; el prestador la acepta y pasa a Confirmada,
luego En camino, En servicio y Finalizada; el cliente paga por la pasarela y
al final califica. Las entidades que modelaré en la Semana 14 son Rubro,
Prestador, Cliente, Solicitud, SeguimientoSolicitud, Pago y Calificación.

Creé las apps servicios, clientes y solicitudes; los prestadores ya tenían su
app chamba desde el Lab 12. En React agregué las páginas vacías del panel y
armé el mapa de rutas, por ejemplo `/api/solicitudes/` con `/solicitudes`."

## 7. Cierre

"`manage.py check`, `npm run lint` y `npm run build` terminan sin errores, y
el README del repositorio guarda todo el diseño de las dos partes. La idea con
la que me quedo es que una aplicación empresarial se diseña antes de
programarse: si las reglas y las rutas están claras desde ahora, en la Semana
14 solo queda escribir los modelos y la API que ya sabemos que necesitamos."
