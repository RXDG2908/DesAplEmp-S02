# Guión expositivo — Laboratorio 8, Parte 1 (Veterinaria)

Guión para exponer en voz alta lo que se hizo en la parte del laboratorio
correspondiente a la aplicación de la veterinaria, indicando en qué archivo
está cada cosa.

## Introducción

"En este laboratorio no se creó ninguna entidad nueva ni se tocó
[`models.py`](../../django_project/src/vet/models.py). Lo que se hizo fue exponer las citas y los insumos que ya
existían como una API REST que responde en JSON, para que otro programa,
como una app móvil o React, pueda usarlos. Todo el trabajo está en tres
archivos nuevos de la app: [`vet/serializers.py`](../../django_project/src/vet/serializers.py), [`vet/api_views.py`](../../django_project/src/vet/api_views.py) y
[`vet/api_urls.py`](../../django_project/src/vet/api_urls.py), más dos líneas en la configuración del proyecto."

## Arquitectura: cómo funciona y para qué sirve

"Ahora la arquitectura. Una API REST sirve para que otro programa, como React o una app móvil, use nuestros datos. En vez de devolver HTML con un Template, devolvemos JSON y un código HTTP. Eso separa el backend del frontend: el mismo backend puede alimentar a varios clientes.

El recorrido es este. El cliente hace, por ejemplo, GET a `/api/citas/`. [`config/urls.py`](../../django_project/src/config/urls.py) lo manda a [`vet/api_urls.py`](../../django_project/src/vet/api_urls.py), donde el router, que es un `DefaultRouter`, genera solo las rutas de lista, detalle y la raíz de la API. La ruta llega a un ViewSet en [`vet/api_views.py`](../../django_project/src/vet/api_views.py), que decide qué hacer según el verbo HTTP: GET lista o muestra, POST crea, PUT y PATCH modifican, DELETE elimina. El ViewSet usa un serializer, de [`vet/serializers.py`](../../django_project/src/vet/serializers.py), que es el equivalente al formulario pero para la API: convierte el modelo a JSON y valida el JSON que llega, como la regla de que el stock sea de al menos uno. Debajo siguen el Model y el ORM de siempre, sin cambios en [`vet/models.py`](../../django_project/src/vet/models.py).

Lo importante: no se duplicó ninguna regla. El filtro `?estado=` y la acción `proximas` reutilizan los métodos del QuerySet del Laboratorio 7, y con `select_related` y `prefetch_related` la API de citas bajó de 24 consultas a 3. Las citas son solo lectura porque solo se consultan. Lo que falta es la seguridad: por ahora la API está abierta."

## 1. Instalación de Django REST Framework

"Primero se instaló el paquete con `pip install djangorestframework`. En
[`config/settings.py`](../../django_project/src/config/settings.py), dentro de `INSTALLED_APPS`, se agregó la línea
`'rest_framework'`, y en [`requirements.txt`](../../django_project/src/requirements.txt) se agregó
`djangorestframework==3.18.3`. En [`config/urls.py`](../../django_project/src/config/urls.py) se agregó la línea
`path('api/', include('vet.api_urls'))`, que hace que todo lo que empiece
con `/api/` lo maneje la API de la veterinaria."

## 2. El serializer del insumo y su validación

"En [`vet/serializers.py`](../../django_project/src/vet/serializers.py) está la clase `InsumoSerializer`, que hereda de
`ModelSerializer`. En su `Meta` se indica el modelo `Insumo` y los campos
id, nombre, unidad y stock. Un serializer es para la API lo que un
formulario es para las páginas: convierte el objeto a JSON y valida lo que
llega. Dentro de esa misma clase está el método `validate_stock`, que es
nuestra regla de negocio: un insumo no se puede registrar con stock menor a
1. DRF lo ejecuta solo cuando se llama a `is_valid()`."

## 3. Los serializers anidados de la cita

"Más abajo, en el mismo archivo, están `VeterinarioSerializer`,
`FichaClinicaSerializer` y `ConsumoInsumoSerializer`, y al final
`CitaSerializer`. En `CitaSerializer` se usan los otros tres como campos:
`veterinario` para la relación uno a muchos, `ficha` para la relación uno a
uno, que puede salir `null`, y `consumos` con `many=True` para la relación
muchos a muchos. Así, al pedir una cita, el JSON trae también los datos de
su veterinario, su ficha y los insumos que consumió."

## 4. Las vistas genéricas (primera versión)

"En [`vet/api_views.py`](../../django_project/src/vet/api_views.py), arriba del todo, están `InsumoListCreate` e
`InsumoDetail`. Fueron la primera versión, con vistas genéricas: la primera
lista y crea insumos, la segunda ve, edita y borra uno. Se dejaron en el
archivo como referencia, pero ya no se usan: sus rutas están comentadas al
final de [`vet/api_urls.py`](../../django_project/src/vet/api_urls.py)."

## 5. El ViewSet del insumo

"Debajo está `InsumoViewSet`, que hereda de `ModelViewSet` y reemplaza a las
dos vistas anteriores en una sola clase. Además tiene `filter_backends` con
`SearchFilter` y `OrderingFilter`, `search_fields` con nombre y unidad, y
`ordering_fields` con nombre y stock. Eso es lo que permite usar
`?search=` y `?ordering=` en la URL."

## 6. El ViewSet de la cita

"Al final de [`vet/api_views.py`](../../django_project/src/vet/api_views.py) está `CitaViewSet`, que hereda de
`ReadOnlyModelViewSet`, por eso solo permite consultar. En su método
`get_queryset()` se usan `select_related` para el veterinario y la ficha, y
`prefetch_related` para los consumos y sus insumos; con eso la consulta de
todas las citas bajó de 24 a 3 consultas a la base de datos. En ese mismo
método se lee el parámetro `?estado=` y se aplica con `con_estado()`, que es
el método del QuerySet personalizado de la Semana 7, que está en
[`vet/models.py`](../../django_project/src/vet/models.py). Y debajo está la acción `proximas`, marcada con
`@action(detail=False)`, que llama a `proximas()` del mismo QuerySet y crea
la ruta `/api/citas/proximas/`."

## 7. El router

"En [`vet/api_urls.py`](../../django_project/src/vet/api_urls.py) se crea un `DefaultRouter` y se registran los dos
ViewSets con `router.register('insumos', ...)` y
`router.register('citas', ...)`. El router genera solo las rutas de lista y
de detalle de cada recurso, y además la raíz `/api/`, que muestra los
recursos disponibles."

## 8. Verificación

"La verificación se hizo de tres formas. En el shell de Django se probó el
serializer con un dato válido y uno inválido. Con `curl` se probó el CRUD
completo del insumo y se obtuvieron los códigos 200, 201, 400, 204 y 404.
Y en el navegador, con la API navegable de DRF, se probaron la búsqueda, el
ordenamiento, el filtro por estado y la acción de citas próximas, incluso
combinando parámetros con `&`. El conteo de consultas se midió con el
script [`medir_api_n1.py`](../../django_project/src/medir_api_n1.py), que está en la carpeta `src`."

## Cierre

"En resumen, la API vive en tres archivos de `vet`: [`serializers.py`](../../django_project/src/vet/serializers.py)
convierte y valida, [`api_views.py`](../../django_project/src/vet/api_views.py) decide qué datos se entregan y cómo se
filtran, y [`api_urls.py`](../../django_project/src/vet/api_urls.py) conecta todo con el router bajo `/api/`. No se
cambió ningún modelo: la API reutiliza las relaciones y el QuerySet que ya
existían. Lo que le falta todavía es seguridad, porque por ahora
cualquiera puede modificar los datos."
