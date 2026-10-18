# Informe — Laboratorio 08: Django REST Framework

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Lucas Inga - Renzo Leon
**Repositorio:** https://github.com/RXDG2908/DesAplEmp-S02

En este laboratorio no se agregaron entidades nuevas: las que ya existían en la
app vet se expusieron como una API REST que responde en JSON. La API reutiliza
el mismo Model, las mismas relaciones y el CitaQuerySet de la Semana 7. Este
informe cubre la **Parte 1 (app vet)**, que desarrolló Renzo León. La Parte 2
(investigación propia) corresponde a Lucas Inga.

Recorrido de una petición a la API:

```
Cliente (navegador o curl) → /api/citas/ → DefaultRouter → CitaViewSet
→ CitaSerializer → CitaQuerySet → Django ORM → SQLite → Response (JSON + código)
```

Las capturas están en `Capturas/Lab08/`.

## PARTE 1 — Una API REST sobre la app vet

### Ejercicio 1 — Instalar Django REST Framework e identificar los recursos

Tabla de equivalencias con la clase:

| Concepto de la clase | En la app vet |
|---|---|
| Recurso simple con regla de negocio (Producto, precio > 0) | **Insumo**: el stock inicial debe ser de al menos 1 unidad |
| Recurso con relaciones, de solo lectura (Pedido con detalles) | **Cita** con su veterinario (1:N), su ficha clínica (1:1) y sus consumos de insumo (N:M con modelo intermedio) |
| Campo de estado para `?estado=` | `Cita.estado` (Pendiente, Confirmada, Atendida) |
| Método del QuerySet personalizado (`pagados()`) | `CitaQuerySet.proximas()` y `con_estado()` de la Semana 7 |

El campo de estado y el QuerySet personalizado ya existían desde la Semana 7,
así que no hubo que crear nada nuevo en los modelos ni migraciones. Se instaló
el paquete con `pip install djangorestframework` (versión 3.18.3), se agregó
`'rest_framework'` a `INSTALLED_APPS` y se añadió la línea al
`requirements.txt`.

Capturas: `ej1_pip.png`, `ej1_settings.png`.

### Ejercicio 2 — Crear un ModelSerializer y serializar en el shell

En `vet/serializers.py` se creó `InsumoSerializer`, un ModelSerializer con los
campos id, nombre, unidad y stock. En el shell se serializó primero un solo
insumo (la jeringa de 5 ml) y se obtuvo un diccionario; luego se serializó el
QuerySet completo con `many=True` y se obtuvo una lista de diccionarios.

**¿Por qué many=True?** Sin esa opción el serializer espera un solo objeto y
trata de leer sus campos directamente; un QuerySet es una colección y no tiene
un campo `nombre` ni `stock`. Con `many=True` el serializer recorre la
colección y aplica la conversión a cada elemento, devolviendo una lista.

Capturas: `ej2_serializer.png`, `ej2_shell.png`.

### Ejercicio 3 — Deserializar y validar

Se agregó al serializer el método `validate_stock`: un insumo nuevo debe
registrarse con al menos 1 unidad en stock. DRF llama a este método solo
dentro de `is_valid()`.

- **Caso inválido** (suero fisiológico con stock 0): `is_valid()` devolvió
  `False` y `errors` mostró "El stock inicial debe ser de al menos 1 unidad."
- **Caso válido** (suero fisiológico con stock 40): `is_valid()` devolvió
  `True`, `validated_data` trajo los tres campos limpios y `save()` creó el
  insumo con id 7.

Captura: `ej3_shell.png`.

### Ejercicio 4 — Exponer el recurso con vistas genéricas

En `vet/api_views.py` se crearon `InsumoListCreate` (ListCreateAPIView) y
`InsumoDetail` (RetrieveUpdateDestroyAPIView), y se enlazaron en
`/api/insumos/` y `/api/insumos/<pk>/`. La API navegable de DRF mostró la lista
con los métodos permitidos GET y POST, y el detalle con GET, PUT, PATCH y
DELETE, junto a un formulario para editar.

Las dos clases siguen en `api_views.py` como referencia, pero sus rutas
quedaron comentadas en `vet/api_urls.py` porque en el Ejercicio 5 se
reemplazaron por el ViewSet.

Capturas: `ej4_views.png`, `ej4_lista_generica.jpg`, `ej4_detalle_generico.jpg`.

### Ejercicio 5 — Reemplazar las vistas por un ViewSet y un router

Las dos vistas genéricas se reemplazaron por `InsumoViewSet` (ModelViewSet),
registrado en un `DefaultRouter` en `vet/api_urls.py`; `config/urls.py` monta
ese archivo en `/api/`. Al abrir `/api/` aparece la raíz de la API con los dos
recursos registrados: `insumos` y `citas`.

Sin escribir ninguna ruta a mano, el router generó:

| Ruta | Métodos | Acción |
|---|---|---|
| `/api/` | GET | Raíz con la lista de recursos |
| `/api/insumos/` | GET, POST | Listar y crear |
| `/api/insumos/<pk>/` | GET, PUT, PATCH, DELETE | Ver, reemplazar, modificar y borrar |
| `/api/citas/` | GET | Listar (solo lectura) |
| `/api/citas/<pk>/` | GET | Ver una cita |
| `/api/citas/proximas/` | GET | Acción propia del Ejercicio 8 |

El ViewSet reúne en una sola clase lo que antes eran dos vistas, y el router
crea las dos URLs (lista y detalle) a partir del nombre con que se registra.

Capturas: `ej5_viewset.png`, `ej5_urls.png`, `ej5_api_root.jpg`.

### Ejercicio 6 — Probar el CRUD y los códigos de estado

Las pruebas se hicieron con curl contra el servidor de desarrollo:

| # | Petición | Código | Resultado |
|---|---|---|---|
| 1 | GET `/api/insumos/` | **200 OK** | Lista de los 5 insumos |
| 2 | GET `/api/insumos/1/` | **200 OK** | Jeringa 5ml, stock 100 |
| 3 | POST `/api/insumos/` con "Collar isabelino", stock 12 | **201 Created** | Insumo creado con id 9 |
| 4 | POST `/api/insumos/` con nombre vacío y stock 0 | **400 Bad Request** | Errores en nombre ("no puede estar en blanco") y en stock (regla del validate_stock) |
| 5 | PATCH `/api/insumos/9/` con stock 20 | **200 OK** | Stock actualizado a 20 |
| 6 | DELETE `/api/insumos/9/` | **204 No Content** | Insumo borrado, sin cuerpo |
| 7 | GET `/api/insumos/9/` | **404 Not Found** | "No Insumo matches the given query." |

Capturas: `ej6_1_list.png` a `ej6_7_404.png`.

**Diferencia con un Template.** Un Template devuelve una página HTML ya armada
para que la lea una persona en el navegador. La API devuelve solo los datos en
JSON, con un código de estado que dice si la operación salió bien; quien la
consume (una app móvil, React en la Semana 9 o cualquier otro programa) decide
cómo mostrarlos. Por eso los errores de validación llegan como un objeto JSON
con un 400, en lugar de un formulario con mensajes en rojo.

**Por qué la API está abierta.** No se configuró autenticación ni permisos,
así que DRF usa su permiso por defecto (`AllowAny`): cualquiera que conozca la
URL puede crear, modificar o borrar insumos sin iniciar sesión. Queda así
hasta que se trabaje la seguridad (autenticación por token o sesión y
permisos por usuario).

### Ejercicio 7 — Un recurso de solo lectura con relaciones anidadas

`CitaSerializer` anida tres serializers: `VeterinarioSerializer` (la FK),
`FichaClinicaSerializer` (el 1:1, que sale como `null` si la cita todavía no
tiene ficha) y `ConsumoInsumoSerializer` con `many=True` (el modelo intermedio,
con el nombre del insumo, la cantidad, el precio y el subtotal). El recurso se
expone con `CitaViewSet` (ReadOnlyModelViewSet), por eso solo admite GET.

En `get_queryset()` se usa `select_related('veterinario', 'ficha')` para las
relaciones de a uno y `prefetch_related('consumos__insumo')` para la de a
muchos.

Medición con `medir_api_n1.py` (serializa las 5 citas con sus relaciones y
cuenta `connection.queries`):

| Queryset | Consultas |
|---|---|
| `Cita.objects.all()` | **24** |
| Con `select_related` + `prefetch_related` | **3** |

Sin optimizar, la serialización hace 1 consulta para las citas, 5 para los
veterinarios, 5 para las fichas, 5 para los consumos y 8 para el insumo de cada
consumo (1 + 5 + 5 + 5 + 8 = 24). Optimizado son 3: una con JOIN para citas,
veterinarios y fichas, una para todos los consumos y una para todos los
insumos. La cantidad ya no crece con el número de citas.

Capturas: `ej7_serializer.png`, `ej78_citaviewset.png`, `ej7_script.png`,
`ej7_resultado.png`, `ej7_cita_detalle.jpg`.

### Ejercicio 8 — Búsqueda, ordenamiento, filtro por parámetro y acción propia

- `InsumoViewSet` tiene `SearchFilter` (busca en nombre y unidad) y
  `OrderingFilter` (ordena por nombre o stock).
- `CitaViewSet.get_queryset()` lee `?estado=` y lo aplica con
  `con_estado()` del CitaQuerySet.
- La acción `@action(detail=False)` `proximas` reutiliza
  `CitaQuerySet.proximas()` (citas con fecha de hoy en adelante) sobre el
  queryset ya optimizado, así que también respeta `?estado=`.

| URL | Resultado |
|---|---|
| `/api/insumos/?search=gasa` | 1 insumo: Gasa estéril |
| `/api/insumos/?ordering=-stock` | Jeringa (100), Gasa (45), Suero (40), Antibiótico (30), Vacuna (25) |
| `/api/insumos/?search=in&ordering=-stock` | Combina ambos con `&`: Jeringa (100) y Antibiótico inyectable (30) |
| `/api/citas/?estado=Pendiente` | 1 cita: Luna |
| `/api/citas/proximas/` | 2 citas desde el 18/10/2026: Luna (20/10) y Toby (21/10) |
| `/api/citas/proximas/?estado=Confirmada` | Combina la acción con el filtro: solo Toby |

Capturas: `ej8_search.jpg`, `ej8_ordering.jpg`, `ej8_search_ordering.jpg`,
`ej8_estado.jpg`, `ej8_proximas.jpg`, `ej8_proximas_estado.jpg`.

## Qué resuelve la API y qué le falta

Los Templates muestran páginas a una persona y el Admin es una herramienta
interna para administrar datos; ninguno de los dos sirve para que otro
programa lea o escriba información. La API entrega los mismos datos en JSON,
con códigos de estado estándar, y así una app móvil o un frontend en React
puede consumirlos sin depender del HTML. Además reutiliza lo que ya estaba
hecho: los modelos, las relaciones, las optimizaciones de consultas y el
QuerySet personalizado.

Le falta todavía la seguridad: no hay autenticación ni permisos, por lo que
cualquiera puede modificar los insumos. También falta paginar las listas
(hoy devuelven todos los registros de una vez) y configurar CORS para que un
frontend en otro puerto, como React, pueda llamarla desde el navegador.

## Conclusiones

- Un serializer cumple para la API el papel del Form: convierte los objetos a
  JSON y valida lo que llega con reglas propias como `validate_stock`.
- Con un ModelViewSet y un DefaultRouter se obtiene el CRUD completo con
  muy poco código, en lugar de escribir cada vista y cada ruta.
- Los serializers anidados pueden causar el problema N+1; con
  `select_related` y `prefetch_related` en `get_queryset()` se bajó de 24 a 3
  consultas.
- Los filtros y la acción propia reutilizan el CitaQuerySet de la Semana 7: la
  API no reemplaza al ORM, lo aprovecha.
