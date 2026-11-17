# Exposición — Laboratorio 12: Ajax con Axios, de la API de Django a React (insumos y panel de Chamba PE)

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiante:** Renzo León
**Tema:** conectar React con Django. React pide los datos a la API REST con
una petición Ajax (Axios), los muestra sin recargar la página y envía los
cambios con POST, PATCH y DELETE. Se aplica primero sobre el recurso
**insumos** de la veterinaria (Parte 1) y después sobre el panel de
**Chamba PE** (Parte 2).

> Django y React son **dos aplicaciones distintas** que corren a la vez
> (puertos **8000** y **5173**) y se comunican por HTTP.

---

## De dónde partimos

Hasta el Laboratorio 11 los datos estaban **escritos a mano** en
[`datos.js`](../../frontend/src/datos.js) y se perdían al recargar. La API de la Semana 8 ya existía, pero React
no la usaba. Ahora React deja de inventar los datos y se los **pide** a
Django.

```
Lab 11:  datos.js (a mano)  →  PanelPrestadores (estado)  →  pantalla
Lab 12:  SQLite → ORM → Serializer → ViewSet  ⇄ HTTP (JSON) ⇄  Axios → PanelPrestadores → pantalla
```

## Arquitectura: cómo funciona y para qué sirve

**Idea central.** **React no reemplaza a Django.** Django entrega y valida los
datos (serializer y ViewSet); React los pide, los dibuja y envía los cambios.
Lo que antes resolvía un Template recargando la página, ahora lo resuelve una
**petición Ajax** y un **cambio de estado**.

```
Navegador (localhost:5173)                       Django (127.0.0.1:8000)
 PanelPrestadores                                 /api/chamba/prestadores/
   useEffect → api.get(...)   ── GET  ──────────▶  ViewSet → ORM → SQLite
   setPrestadores(datos)      ◀── 200 + JSON ───   Serializer (a JSON)
   onGuardar → api.post(...)  ── POST ──────────▶  Serializer.validate_tarifa
                              ◀── 201 / 400 ────
```

| Pieza | Para qué sirve | Archivo |
|---|---|---|
| **CORS** | Autoriza al origen de React a **leer** las respuestas de Django | [`settings.py`](../../django_project/src/config/settings.py) |
| **Instancia de Axios** | `baseURL` y `timeout` en **un solo lugar** | [`api.js`](../../frontend/src/api.js) |
| **GET en `useEffect`** | Pide la lista **después** de dibujar, y otra vez cuando cambia el filtro | [`ListaPractica`](../../frontend/src/practica/ListaPractica.jsx), [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) |
| **Cargando / error / vacío** | La pantalla nunca queda en blanco | [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) |
| **POST / PATCH / DELETE** | Crear, editar y eliminar; el estado se actualiza **solo si la API responde bien** | [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) |
| **Errores 400 y 404** | Se muestran al usuario con `textoError()` | [`api.js`](../../frontend/src/api.js), [`PrestadorForm`](../../frontend/src/components/PrestadorForm.jsx) |
| **Parámetros** | `?search=` y `?estado=` viajan a la API, que filtra | [`chamba/api_views.py`](../../django_project/src/chamba/api_views.py) |

**El recorrido de una petición, en una frase:** *React decide cuándo pedir,
Axios envía la petición, el ViewSet decide la operación, el serializer valida
y convierte a JSON, y el ORM habla con SQLite.*

1. `PanelPrestadores` se dibuja con `cargando = true` y muestra **Cargando...**.
2. Su efecto llama a `api.get('/chamba/prestadores/', { params })`.
3. El `PrestadorViewSet` filtra con `?search=` y `?estado=` y el serializer devuelve el JSON con **200**.
4. La función **adaptadora** convierte la tarifa de texto (`"60.00"`) a número y se guarda en el estado.
5. Al registrar, `api.post(...)` responde **201** y el prestador se agrega con un arreglo nuevo; si la tarifa es 0, responde **400** y el formulario muestra el mensaje.
6. Al eliminar, el primer clic pide **Confirmar**; el segundo envía **DELETE** (204) y se quita con `filter`.

**Por qué se diseñó así:**

- **Una sola instancia de Axios**: si cambia el servidor se edita una línea, no todos los componentes.
- **La petición en un efecto**: en el cuerpo del componente se repetiría en cada dibujo, sin fin.
- **El estado cambia después de la respuesta**: la pantalla muestra lo que de verdad quedó guardado.
- **La validación final es del servidor**: el navegador ayuda, pero `validate_tarifa` es la regla que manda.
- **Limitación**: la API todavía está **abierta a cualquiera**; faltan la autenticación y los permisos.

---

# PARTE 1 — Ajax con el recurso `insumos` (`src/practica`)

## Paso 1 — Verificar la API y reconocer la petición (Ejercicio 1)

Con `python manage.py runserver`, `GET http://127.0.0.1:8000/api/insumos/`
responde **200** con una lista JSON (`id`, `nombre`, `unidad`, `stock`).

| Operación | Método | URL | Código esperado |
|---|---|---|---|
| Listar | GET | `/api/insumos/` | 200 |
| Ver uno | GET | `/api/insumos/<id>/` | 200 (404 si no existe) |
| Crear | POST | `/api/insumos/` | 201 (400 si `stock` < 1) |
| Modificar | PATCH / PUT | `/api/insumos/<id>/` | 200 |
| Eliminar | DELETE | `/api/insumos/<id>/` | 204 |

**Diferencia con un Template:** la API no entrega una página, solo **datos en
JSON y un código de estado**; quien decide cómo dibujarlos es React. El
Template mezcla los datos con el HTML en el servidor y devuelve la página
completa.

## Paso 2 — Configurar CORS (Ejercicio 2)

Un `fetch` desde `localhost:5173` fue **bloqueado por CORS**. Se instaló
`django-cors-headers` (y se actualizó `requirements.txt`), se agregó
`corsheaders` a `INSTALLED_APPS`, `CorsMiddleware` **en la parte alta** de
`MIDDLEWARE` y `CORS_ALLOWED_ORIGINS = ['http://localhost:5173']`. Al
repetir, la respuesta fue **200**.

**Por qué ocurre:** para el navegador, otro **puerto** es otro **origen**, y
por seguridad no deja que una página lea datos de otro origen si el servidor
no lo autoriza. La petición sí llega a Django; lo que se bloquea es la
**lectura** de la respuesta.

## Paso 3 — Axios y una instancia (Ejercicio 3)

`npm install axios` y [`src/api.js`](../../frontend/src/api.js) con
`axios.create({ baseURL: 'http://127.0.0.1:8000/api', timeout: 5000 })`. La
ventaja es que **la dirección del servidor se escribe una sola vez**; los
componentes usan rutas cortas como `/insumos/`.

## Paso 4 — GET con `useEffect` (Ejercicio 4)

[`ListaPractica`](../../frontend/src/practica/ListaPractica.jsx) pide la lista con `await api.get('/insumos/')` dentro de un efecto,
la guarda en el estado y la dibuja con `map()` y `key`. En Network: **GET
200**.

- **Va en un efecto** porque el cuerpo del componente se ejecuta en cada
  dibujo: la respuesta cambiaría el estado, se dibujaría otra vez y volvería
  a pedir sin parar.
- **La función del efecto no es `async`** porque un efecto solo puede
  devolver nada o una función de limpieza, y una `async` devuelve una
  promesa. Por eso se declara `cargar()` dentro y se la llama.

## Paso 5 — Cargando, error y lista vacía (Ejercicio 5)

Con `try`, `catch` y `finally`:

| Estado | La pantalla muestra |
|---|---|
| Esperando la respuesta | **Cargando...** |
| La petición falla (Django apagado) | **No se pudo cargar la lista** (y el error en consola) |
| Responde bien, sin datos | **No hay insumos registrados** |

No se deja la pantalla en blanco porque la persona no sabría si está
cargando, si falló o si no hay datos.

## Paso 6 — POST con formulario controlado (Ejercicio 6)

El formulario envía `api.post('/insumos/', ...)` y agrega `respuesta.data`
con un arreglo nuevo. Válido → **POST 201** y aparece sin recargar. Con stock
0 → **400** y la pantalla muestra el mensaje de `validate_stock` (Semana 8):
*"El stock inicial debe ser de al menos 1 unidad."* El texto sale de
`err.response.data` mediante `textoError()`.

## Paso 7 — DELETE y PATCH (Ejercicio 7)

- **Eliminar** → `api.delete(...)` → **204** → se quita del estado con `filter()`.
- **+1 stock** → `api.patch(..., { stock: stock + 1 })` → **200** → se reemplaza con `map()`.

## Paso 8 — Búsqueda y verificación (Ejercicio 8)

El buscador envía `params: { search: buscar }` y el efecto tiene `[buscar]`.
En Network: `http://127.0.0.1:8000/api/insumos/?search=gasa`. `npm run lint`
y `npm run build` sin errores.

**Qué hace cada pieza:** React muestra la pantalla y decide cuándo pedir;
Axios envía la petición HTTP; el ViewSet decide la operación; el serializer
valida y convierte a JSON; el ORM consulta SQLite. **La API sigue abierta a
cualquiera** porque no tiene autenticación ni permisos.

---

# PARTE 2 — Panel de Chamba PE contra su propia API

## Paso 9 — El recurso del panel (Ejercicio 9)

| Elemento | En Chamba PE |
|---|---|
| Entidad principal | Prestador |
| URL de la API | `/api/chamba/prestadores/` |
| Campos | `id`, `nombres`, `apellidos`, `rubro`, `tarifa` (decimal, llega como texto) y `estado` |
| Regla para el 400 | `validate_tarifa`: la tarifa debe ser **mayor que cero** |
| Filtros | `?search=` (nombres y apellidos), `?estado=` y `?ordering=` (tarifa o apellidos) |
| Operaciones | Listar, crear, editar, aprobar o suspender (PATCH) y eliminar |

El panel del Lab 11 usaba datos a mano y la API **no tenía este recurso**, así
que se agregó la app [`chamba`](../../django_project/src/chamba/models.py): el modelo `Prestador`, su [serializer](../../django_project/src/chamba/serializers.py) con
`validate_tarifa`, un [`ModelViewSet`](../../django_project/src/chamba/api_views.py) con búsqueda, filtro y orden, y la ruta
[`/api/chamba/prestadores/`](../../django_project/src/config/urls.py). Los seis prestadores se cargan con
[`cargar_chamba.py`](../../django_project/src/cargar_chamba.py).

## Paso 10 — Listado desde la API (Ejercicio 10)

[`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) reemplaza los datos a mano por un **GET en un efecto** con la
instancia `api`. Guarda los prestadores y los estados `cargando` y `error`, y
entrega los datos al listado por props. La función **`adaptar()`** convierte
la tarifa de texto a número. En Network: **GET 200**. Con Django apagado:
**No se pudo cargar la lista de prestadores**.

## Paso 11 — Alta y edición con POST y PATCH (Ejercicio 11)

- **Alta:** [`PrestadorForm`](../../frontend/src/components/PrestadorForm.jsx) llama a `onGuardar` → `api.post(...)` → se agrega con un arreglo nuevo.
- **Edición:** **Editar** en una fila guarda el prestador en `editando`, el formulario se llena con sus datos (gracias a `key={editando.id}`) y al enviar se ejecuta `api.patch(...)`; el estado se actualiza con `map()`.
- **Aprobar / Suspender** también envían un PATCH con el nuevo estado.
- Los **400** del serializer se muestran junto al formulario.

Códigos obtenidos: **201** al crear a Pedro Soto · **400** con tarifa 0 ·
**200** al editar a Pedro (tarifa 48, rubro Electricidad) y al aprobar a
María Torres.

## Paso 12 — Eliminar con confirmación (Ejercicio 12)

El primer clic en **Eliminar** cambia el botón a **Confirmar**; solo el
segundo ejecuta el DELETE. Con **204** se quita con `filter()`. Si responde
**404** (ya no existe), el panel avisa y lo quita de la lista.

Prueba del 404: se creó un prestador temporal, se borró directamente en la
API y luego se pulsó Eliminar → Confirmar en la pantalla, que todavía lo
mostraba. En Network aparece antes una petición **OPTIONS**: es la consulta
previa (*preflight*) de CORS.

## Paso 13 — Búsqueda, filtros y resumen con la API (Ejercicio 13)

[`BuscadorPrestadores`](../../frontend/src/components/BuscadorPrestadores.jsx) y [`FiltroEstadoPrestador`](../../frontend/src/components/FiltroEstadoPrestador.jsx) envían sus valores como parámetros y el
efecto depende de `[busqueda, estado]`. [`ResumenPrestadores`](../../frontend/src/components/ResumenPrestadores.jsx) calcula total,
conteo por estado y tarifa promedio con los datos de la API. **Opcional
hecho:** la limpieza del efecto cancela la petición pendiente con
`AbortController`.

| URL generada | Resultado |
|---|---|
| `/api/chamba/prestadores/?search=ro&estado=` | Rosa Díaz y Pedro Soto |
| `/api/chamba/prestadores/?search=&estado=Aprobado` | Solo los aprobados |
| `/api/chamba/prestadores/?search=a&estado=Aprobado` | Combina los dos parámetros con `&` |
| `?search=zzz` | Lista vacía → **No hay prestadores que coincidan** |

## Paso 14 — Verificar y publicar (Ejercicio 14)

Consola sin advertencias, Django sin errores 500, `npm run lint` y
`npm run build` sin errores, y `node_modules` y `dist` ignorados.

**Qué resuelve Ajax frente a los Templates:** el panel se actualiza **sin
recargar la página**; React pide solo los datos y cambia lo necesario,
mientras Django valida y guarda. **Qué falta:** autenticación y permisos; hoy
cualquiera que conozca la dirección puede crear, editar o eliminar
prestadores, y ese panel solo debería usarlo el administrador de Chamba PE.

## Resumen para el checklist

| Criterio | Dónde |
|---|---|
| CORS configurado, `requirements.txt` y dos servidores a la vez | [`settings.py`](../../django_project/src/config/settings.py) |
| Axios con `baseURL` en `src/api.js` | [`api.js`](../../frontend/src/api.js) |
| Listado con GET dentro de `useEffect` | [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx) |
| Estados de carga, error y lista vacía | [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx), [`PrestadorListado`](../../frontend/src/components/PrestadorListado.jsx) |
| POST con arreglo nuevo, sin recargar | `guardarPrestador` |
| Errores 400 junto al formulario | [`PrestadorForm`](../../frontend/src/components/PrestadorForm.jsx), `textoError()` |
| PATCH para editar y DELETE (204) con confirmación | `cambiarEstado`, `eliminarPrestador` |
| Parámetros `?search=` y `?estado=` que recargan la lista | [`PanelPrestadores`](../../frontend/src/components/PanelPrestadores.jsx), [`chamba/api_views.py`](../../django_project/src/chamba/api_views.py) |
| Consola limpia, lint y build sin errores, sin 500 | Paso 14 |
