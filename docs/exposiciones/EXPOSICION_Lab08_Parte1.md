# Exposición — Laboratorio 08, Parte 1: API REST con Django REST Framework sobre la app `vet`

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** exponer la app `vet` (reserva de citas de veterinaria) como una API
REST que entrega JSON, reutilizando los Models, las relaciones y el QuerySet
personalizado construidos en semanas anteriores.

> Este documento explica, en el orden en que se hicieron, todos los pasos de
> la Parte 1 del Laboratorio 8. La idea es poder exponérselo al profesor
> contando la historia completa: de dónde veníamos, qué se hizo en cada paso
> y por qué, sin necesitar leer el código en paralelo.

---

## De dónde partimos

Antes de este laboratorio la app `vet` ya tenía un camino largo recorrido:
nació en el Laboratorio 2 con datos en memoria, en el Laboratorio 3 pasó a un
Model real en SQLite, en el Laboratorio 4 se le agregaron las tres relaciones
(la ficha clínica **uno a uno**, el veterinario **uno a muchos** y los insumos
**muchos a muchos** a través de `ConsumoInsumo`), en el Laboratorio 5 se
registró en el Django Admin, en el 6 se ordenaron sus Templates y en el 7 se
le agregó el campo de estado de la cita, el registro de consumos con
transacción y el `CitaQuerySet` con los métodos `con_estado()` y `proximas()`.

Hasta aquí todo lo que la aplicación entregaba eran **páginas HTML** pensadas
para una persona frente al navegador. Lo que faltaba era que **otro
programa** —una app móvil, o el frontend en React que se verá en la Semana
9— pudiera leer y escribir esos mismos datos.

Esa es la idea central que atraviesa todo el laboratorio: **la API no
reemplaza al ORM ni a las consultas que ya existían, las reutiliza.** No se
cambió ni una línea de `models.py` y no se creó ninguna migración; todo el
trabajo vive en tres archivos nuevos de `vet`: `serializers.py`,
`api_views.py` y `api_urls.py`.

El recorrido de una petición a la API queda así:

```
Cliente (navegador o curl) → /api/citas/ → DefaultRouter → CitaViewSet
→ CitaSerializer → CitaQuerySet → Django ORM → SQLite → Response (JSON + código)
```

---

## Paso 1 — Instalar DRF y elegir los dos recursos (Ejercicio 1)

Se instaló el paquete con `pip install djangorestframework` (versión
3.18.3), se agregó `'rest_framework'` a `INSTALLED_APPS` en
`config/settings.py` y se añadió la línea `djangorestframework==3.18.3` a
`requirements.txt`, para que cualquiera que clone el repositorio lo instale
con `pip install -r requirements.txt`.

Luego se decidió qué exponer, usando la tabla de equivalencias de la guía
(en clase el ejemplo era una cafetería):

| Concepto de la clase | En la app `vet` |
|---|---|
| Recurso simple con regla de negocio (Producto, precio > 0) | **Insumo**: el stock inicial debe ser de al menos 1 unidad |
| Recurso con relaciones, solo lectura (Pedido con detalles) | **Cita** con su veterinario, su ficha clínica y sus consumos |
| Campo de estado para `?estado=` | `Cita.estado` (Pendiente, Confirmada, Atendida) |
| Método del QuerySet personalizado (`pagados()`) | `CitaQuerySet.proximas()` y `con_estado()` |

Se eligió **Insumo** como recurso simple porque sus campos son planos
(nombre, unidad, stock) y tiene una regla de negocio natural sobre el stock.
Se eligió **Cita** como recurso con relaciones porque es la entidad que
concentra las tres relaciones del Laboratorio 4. El campo de estado y el
QuerySet ya existían desde la Semana 7, así que no hubo que crearlos.

---

## Paso 2 — El primer serializer (Ejercicio 2)

Un **serializer** es, para la API, lo que el `Form` es para las vistas HTML:
convierte un objeto del Model en datos simples que se pueden enviar como
JSON, y en sentido contrario valida los datos que llegan antes de guardarlos.

```python
class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ['id', 'nombre', 'unidad', 'stock']
```

Al heredar de `ModelSerializer`, DRF lee el Model y arma solo los campos y
sus validaciones básicas (por ejemplo, que `nombre` no esté vacío y sea
único). En el shell se probó primero con un solo objeto:

```python
>>> InsumoSerializer(insumo).data
{'id': 1, 'nombre': 'Jeringa 5ml', 'unidad': 'unidad', 'stock': 100}
```

y luego con todo el QuerySet, agregando `many=True`, que devolvió una lista
de diccionarios.

**¿Por qué hace falta `many=True`?** Sin esa opción el serializer espera un
solo objeto y trata de leer `nombre`, `stock`, etc. directamente. Un QuerySet
es una colección: no tiene un `nombre` propio. Con `many=True` el serializer
sabe que tiene que recorrer la colección y aplicar la conversión a cada
elemento.

---

## Paso 3 — Validar con una regla de negocio (Ejercicio 3)

Sobre el mismo serializer se agregó una validación propia:

```python
def validate_stock(self, value):
    if value < 1:
        raise serializers.ValidationError(
            'El stock inicial debe ser de al menos 1 unidad.')
    return value
```

DRF busca automáticamente los métodos que se llamen `validate_<campo>` y los
ejecuta dentro de `is_valid()`. La regla tiene sentido en el negocio: no
tiene lógica dar de alta en el almacén un insumo sin existencias.

En el shell se probaron los dos casos que pide la guía:

- **Inválido** (Suero fisiológico con stock 0): `is_valid()` devolvió
  `False` y `errors` mostró el mensaje de la regla.
- **Válido** (Suero fisiológico con stock 40): `is_valid()` devolvió `True`,
  `validated_data` trajo los tres campos limpios y `save()` creó el insumo
  con id 7 en la base de datos.

Es el mismo patrón que ya conocíamos de los formularios (`is_valid()` →
`cleaned_data` → guardar), solo que aquí se llama `validated_data` y `save()`.

---

## Paso 4 — Primera versión con vistas genéricas (Ejercicio 4)

Para exponer el insumo en la web se crearon dos vistas genéricas de DRF en
`vet/api_views.py`:

```python
class InsumoListCreate(generics.ListCreateAPIView):
    queryset = Insumo.objects.order_by('nombre')
    serializer_class = InsumoSerializer

class InsumoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
```

La primera responde a `/api/insumos/` (GET para listar, POST para crear) y la
segunda a `/api/insumos/<pk>/` (GET, PUT, PATCH y DELETE). Basta con decirle
a cada una qué datos usar (`queryset`) y con qué serializer convertirlos;
DRF se encarga del resto.

Al abrir esas URLs en el navegador apareció la **API navegable** de DRF: una
página que muestra el JSON de respuesta, los métodos permitidos y un
formulario para probar la API sin herramientas extra.

Las dos clases siguen en `api_views.py` como referencia, pero sus rutas
quedaron comentadas en `api_urls.py`, porque en el paso siguiente se
reemplazaron.

---

## Paso 5 — Reemplazar por un ViewSet y un router (Ejercicio 5)

Las dos vistas anteriores se juntaron en una sola clase:

```python
class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.order_by('nombre')
    serializer_class = InsumoSerializer
```

y en `vet/api_urls.py` se registró en un router:

```python
router = DefaultRouter()
router.register('insumos', api_views.InsumoViewSet, basename='insumo')
router.register('citas', api_views.CitaViewSet, basename='cita')
urlpatterns = router.urls
```

Finalmente, en `config/urls.py` se montó todo bajo `/api/` con
`path('api/', include('vet.api_urls'))`.

Sin escribir ninguna ruta a mano, el router generó:

| Ruta | Métodos | Acción |
|---|---|---|
| `/api/` | GET | Raíz con la lista de recursos |
| `/api/insumos/` | GET, POST | Listar y crear |
| `/api/insumos/<pk>/` | GET, PUT, PATCH, DELETE | Ver, reemplazar, modificar y borrar |
| `/api/citas/` | GET | Listar (solo lectura) |
| `/api/citas/<pk>/` | GET | Ver una cita |
| `/api/citas/proximas/` | GET | Acción propia (Paso 8) |

La diferencia con el paso anterior: antes eran dos clases y dos `path()`;
ahora es una sola clase y una línea `register()`. Al abrir `/api/` aparece
la raíz de la API con los dos recursos registrados, `insumos` y `citas`.

---

## Paso 6 — Probar el CRUD y los códigos HTTP (Ejercicio 6)

Con el servidor corriendo se probó todo el CRUD del insumo con `curl`
(cliente de pruebas por línea de comandos):

| # | Petición | Código | Qué significa |
|---|---|---|---|
| 1 | GET `/api/insumos/` | **200 OK** | Lista de los 5 insumos |
| 2 | GET `/api/insumos/1/` | **200 OK** | La jeringa de 5 ml |
| 3 | POST con "Collar isabelino", stock 12 | **201 Created** | Se creó con id 9 |
| 4 | POST con nombre vacío y stock 0 | **400 Bad Request** | Dos errores: nombre en blanco y la regla de `validate_stock` |
| 5 | PATCH `/api/insumos/9/` con stock 20 | **200 OK** | Stock actualizado |
| 6 | DELETE `/api/insumos/9/` | **204 No Content** | Borrado, sin cuerpo de respuesta |
| 7 | GET `/api/insumos/9/` | **404 Not Found** | Ya no existe |

Lo interesante de la prueba 4 es que la regla escrita en el Paso 3 se aplicó
sola: no hubo que llamarla desde la vista.

**¿Qué diferencia hay con un Template?** Un Template devuelve una página HTML
ya armada para que la lea una persona. La API devuelve solo los datos en
JSON y un código de estado que dice si la operación salió bien; quien la
consume decide cómo mostrarlos. Por eso un error de validación llega como un
JSON con código 400, no como un formulario con mensajes en rojo.

**¿Por qué la API está abierta?** Porque todavía no se configuró
autenticación ni permisos. DRF usa por defecto `AllowAny`: cualquiera que
conozca la URL puede crear, modificar o borrar insumos. Queda así hasta que
se trabaje la seguridad en una semana posterior.

---

## Paso 7 — La cita con sus relaciones anidadas (Ejercicio 7)

Para la cita se quería que el JSON trajera **todo junto**: no solo el id del
veterinario, sino sus datos; su ficha clínica; y la lista de insumos
consumidos. Para eso se anidaron serializers:

```python
class CitaSerializer(serializers.ModelSerializer):
    veterinario = VeterinarioSerializer(read_only=True)            # 1:N
    ficha = FichaClinicaSerializer(read_only=True, allow_null=True)  # 1:1
    consumos = ConsumoInsumoSerializer(many=True, read_only=True)   # N:M
```

- El **veterinario** sale como un objeto con nombre, colegiatura y
  especialidad.
- La **ficha clínica** sale como objeto o como `null` si la cita aún no fue
  atendida (`allow_null=True`).
- Los **consumos** salen como lista, con el nombre del insumo, la cantidad,
  el precio unitario y el subtotal (la `@property` del modelo intermedio).

El recurso se expuso con `CitaViewSet`, que hereda de
`ReadOnlyModelViewSet`: solo permite GET, porque la cita se crea y se
atiende desde las pantallas que ya existían.

**El problema N+1 vuelve a aparecer.** Al serializar cada cita, Django va a
buscar su veterinario, su ficha, sus consumos y el insumo de cada consumo —
una consulta por cada cosa. Por eso `get_queryset()` se escribió optimizado:

```python
def get_queryset(self):
    citas = (Cita.objects
             .select_related('veterinario', 'ficha')
             .prefetch_related('consumos__insumo')
             .order_by('fecha', 'hora'))
```

Se midió con el script `medir_api_n1.py`, que serializa las 5 citas y cuenta
`connection.queries`:

| Queryset | Consultas |
|---|---|
| `Cita.objects.all()` | **24** |
| Con `select_related` + `prefetch_related` | **3** |

Sin optimizar: 1 consulta para las citas + 5 veterinarios + 5 fichas + 5
listas de consumos + 8 insumos = 24. Optimizado: una con JOIN para citas,
veterinarios y fichas (relaciones "de a uno"), una para todos los consumos y
una para todos los insumos (relaciones "de a muchos"). Y lo más importante:
con 100 citas seguirían siendo 3.

---

## Paso 8 — Búsqueda, orden, filtro y acción propia (Ejercicio 8)

**En el insumo** se agregaron dos filtros de DRF:

```python
filter_backends = [filters.SearchFilter, filters.OrderingFilter]
search_fields = ['nombre', 'unidad']
ordering_fields = ['nombre', 'stock']
```

Con eso, sin escribir lógica propia, la URL acepta `?search=` (busca texto
en nombre o unidad) y `?ordering=` (ordena por nombre o stock; con `-`
delante, de mayor a menor).

**En la cita** se reutilizó el `CitaQuerySet` de la Semana 7 en dos lugares:

1. En `get_queryset()`, el parámetro `?estado=` se aplica con
   `con_estado()`:
   ```python
   estado = self.request.query_params.get('estado')
   if estado:
       citas = citas.con_estado(estado)
   ```
2. Una **acción propia** con `@action(detail=False)` que crea la ruta
   `/api/citas/proximas/` y llama a `proximas()`:
   ```python
   @action(detail=False)
   def proximas(self, request):
       citas = self.get_queryset().proximas()
       serializer = self.get_serializer(citas, many=True)
       return Response(serializer.data)
   ```
   Como parte de `get_queryset()`, la acción ya llega optimizada y además
   respeta el filtro `?estado=`.

`detail=False` significa que la acción trabaja sobre la colección
(`/api/citas/proximas/`) y no sobre una cita puntual (`/api/citas/1/...`).

Resultados probados:

| URL | Resultado |
|---|---|
| `/api/insumos/?search=gasa` | Gasa estéril |
| `/api/insumos/?ordering=-stock` | Jeringa (100), Gasa (45), Suero (40), Antibiótico (30), Vacuna (25) |
| `/api/insumos/?search=in&ordering=-stock` | Combinados con `&`: Jeringa y Antibiótico inyectable |
| `/api/citas/?estado=Pendiente` | Luna |
| `/api/citas/proximas/` | Luna (20/10) y Toby (21/10) |
| `/api/citas/proximas/?estado=Confirmada` | Acción + filtro: solo Toby |

---

## Cómo se verificó cada paso (resumen de pruebas)

| Paso | Qué se probó | Resultado |
|---|---|---|
| 1 | `python manage.py check` sin errores tras agregar `rest_framework` | Correcto |
| 2 | Serializar un insumo y el QuerySet completo con `many=True` | Correcto |
| 3 | `is_valid()` con stock 0 da False; con stock 40 da True y `save()` crea | Correcto |
| 4 | La API navegable muestra lista y detalle con las vistas genéricas | Correcto |
| 5 | `/api/` muestra los recursos `insumos` y `citas` | Correcto |
| 6 | curl devuelve 200, 201, 400, 200, 204 y 404 en el orden esperado | Correcto |
| 7 | La serialización baja de 24 a 3 consultas con el queryset optimizado | Correcto |
| 8 | `?search=`, `?ordering=`, `?estado=` y `/proximas/` filtran bien, solos y combinados | Correcto |

---

## Conclusión de la Parte 1

El hilo conductor de estos ocho pasos es que **la API no inventó nada
nuevo sobre los datos**: usa el mismo Model `Insumo` y `Cita`, las mismas
relaciones del Laboratorio 4, las mismas optimizaciones `select_related` y
`prefetch_related` del Laboratorio 7 y el mismo `CitaQuerySet`. Lo que
agrega es una nueva forma de entregarlos: JSON con códigos HTTP estándar en
lugar de páginas HTML.

Frente a los Templates y al Admin, la API resuelve que **otro programa**
pueda consumir los datos: los Templates son para el cliente en el navegador
y el Admin es para el personal que administra, pero ninguno de los dos sirve
para una app móvil o un frontend en React. Lo que todavía le falta es
seguridad (autenticación y permisos, hoy cualquiera puede escribir),
paginación de las listas y configuración de CORS para que React, que corre
en otro puerto, pueda llamarla desde el navegador.

> **Nota aparte:** al preparar las pruebas se encontró que algunos registros
> antiguos de la base local (un veterinario, una ficha clínica y dos
> insumos) tenían texto mal codificado (`CirugÃ­a` en vez de `Cirugía`),
> heredado de cargas de semanas anteriores, y que eso duplicaba dos insumos
> al correr el script de carga del Lab 07. Se corrigieron esos registros y se
> eliminaron los duplicados en la base local (que no se sube a Git); no es un
> problema de DRF ni forma parte del alcance de este laboratorio, pero se
> deja anotado por transparencia.
