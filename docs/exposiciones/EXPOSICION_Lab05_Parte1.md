# Exposición — Laboratorio 05, Parte 1: Django Admin sobre la app `vet`

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Renzo León · Lucas Inga
**Tema:** registrar y personalizar en el Django Admin la app `vet` (reserva de
citas de veterinaria), reutilizando las relaciones ya construidas en semanas
anteriores.

> Este documento explica, en el orden en que se hicieron, todos los pasos de
> la Parte 1 del Laboratorio 5. La idea es poder exponérselo al profesor
> contando la historia completa: de dónde veníamos, qué se hizo en cada paso
> y por qué, sin necesitar leer el código en paralelo.

---

## De dónde partimos

Antes de tocar nada de este laboratorio, la app `vet` ya tenía un camino
recorrido: nació en el Laboratorio 2 sin base de datos (una lista en memoria),
en el Laboratorio 3 pasó a tener un Model real persistido en SQLite mediante
el ORM de Django, y en el Laboratorio 4 se le agregaron tres relaciones entre
Models:

- una relación **uno a uno** entre `Cita` y `FichaClinica`,
- una relación **uno a muchos** entre `Veterinario` y `Cita`,
- una relación **muchos a muchos con modelo intermedio** entre `Cita` e
  `Insumo`, a través de `ConsumoInsumo` (que además guarda datos propios de
  esa relación: cuánto insumo se usó y a qué precio).

Todo eso ya estaba migrado y funcionando: las migraciones `0001_initial` y
`0002_...` de `vet` ya estaban aplicadas, y `db.sqlite3` ya tenía la
estructura completa. Lo único que faltaba era exponer esos datos en el panel
de administración de Django, porque `vet/admin.py` todavía no registraba
absolutamente nada.

Esa es la idea central que atraviesa todo el laboratorio: **el Django Admin
no reemplaza al Model ni al ORM, los reutiliza.** No se cambió ni una línea
de `models.py`; todo el trabajo fue de registro y de personalización de cómo
se ve y se administra lo que ya existía.

---

## Paso 1 — Confirmar el punto de partida (Ejercicio 1)

Antes de escribir código se hizo un chequeo de estado: correr
`python manage.py showmigrations vet` para confirmar que las dos migraciones
de `vet` estaban aplicadas (aparecen marcadas con `[X]`), y abrir
`vet/admin.py` para verificar que, en efecto, estaba vacío. Esto deja
constancia de que el Admin no necesitó ninguna migración nueva: solo se
apoyó en la estructura que ya existía desde la Semana 4.

De paso, se repasaron las tres relaciones para tenerlas claras antes de
administrarlas: `FichaClinica.cita` (uno a uno, se borra en cascada si se
borra la cita), `Cita.veterinario` (uno a muchos, si se borra el veterinario
la cita no se pierde, solo queda sin asignar) y `Cita.insumos` a través de
`ConsumoInsumo` (muchos a muchos, con `cantidad` y `precio_unitario` propios
de cada consumo).

---

## Paso 2 — Crear el superusuario y entrar al Admin (Ejercicio 2)

Se creó un superusuario con `python manage.py createsuperuser` y se inició
sesión en `/admin/`. En ese primer ingreso el panel ya mostraba, junto a la
app `biblioteca` del compañero de equipo, la sección de autenticación de
Django (Grupos y Usuarios) — pero todavía nada bajo `vet`, porque no había
nada registrado. Este paso sirvió como línea base: confirmar que el Admin
arranca y funciona antes de empezar a agregarle cosas.

---

## Paso 3 — Registrar los tres modelos principales (Ejercicio 3)

Se registraron en `admin.py` los tres modelos que tiene sentido administrar
como listados independientes: `Cita`, `Veterinario` e `Insumo`.

```python
from django.contrib import admin
from .models import Cita, ConsumoInsumo, FichaClinica, Insumo, Veterinario

admin.site.register(Cita, CitaAdmin)
admin.site.register(Veterinario, VeterinarioAdmin)
admin.site.register(Insumo)
```

Aquí se tomó una decisión importante que vale la pena explicar aparte:
`FichaClinica` y `ConsumoInsumo` **no se registraron por su cuenta**. No
tendría sentido un listado suelto de "fichas clínicas" o de "consumos de
insumos" navegable de forma independiente, porque ambos solo existen en
función de una Cita concreta. En vez de eso, se decidió exponerlos como
Inlines dentro de la propia pantalla de `Cita` — eso es exactamente lo que se
hace en los Pasos 5 y 6.

---

## Paso 4 — Personalizar el listado con `ModelAdmin` (Ejercicio 4)

El registro simple (`admin.site.register(Modelo)`) usa una tabla genérica.
Para que el listado sea realmente útil se reemplazó por una clase
`ModelAdmin` en dos de los tres modelos:

```python
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'dueno', 'servicio', 'fecha', 'hora', 'estado', 'veterinario')
    search_fields = ('mascota', 'dueno')
    list_filter = ('estado', 'servicio', 'fecha')
    inlines = [FichaClinicaInline, ConsumoInsumoInline]

class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'colegiatura', 'especialidad')
    search_fields = ('nombre', 'colegiatura')
```

`list_display` decide qué columnas se ven en el listado (en vez del genérico
`__str__` de cada fila), y `search_fields` habilita la caja de búsqueda de
arriba. Se verificó en el navegador que el listado de Citas ya mostraba las
siete columnas configuradas y que buscar por mascota o por dueño filtraba
correctamente.

---

## Paso 5 — Agregar filtros por el panel lateral (Ejercicio 5)

Sobre la misma `CitaAdmin` se agregó `list_filter = ('estado', 'servicio',
'fecha')`. Esto hace aparecer, a la derecha del listado, un panel con tres
filtros: **Por estado** (Pendiente / Confirmada / Atendida), **Por servicio**
(Consulta / Vacunación / Cirugía / Baño) y **Por fecha** (con los rangos que
Django genera automáticamente: hoy, últimos 7 días, este mes, este año). Se
probó cada filtro contra los datos reales de la base y el listado se reducía
correctamente en cada caso.

---

## Paso 6 — Exponer la relación 1:1 con `StackedInline` (Ejercicio 6)

```python
class FichaClinicaInline(admin.StackedInline):
    model = FichaClinica
    extra = 0
```

Un Inline es la forma que tiene el Admin de editar un modelo relacionado
**desde la misma pantalla** del modelo principal, en vez de mandar a un
listado aparte. Se usó `StackedInline` (los campos uno debajo del otro, como
un mini-formulario) porque la relación es 1:1: cada Cita tiene, como mucho,
una Ficha Clínica. Al abrir una Cita desde el Admin, apareció una sección
"Ficha clínica" con los campos `peso_kg`, `diagnostico`, `tratamiento` y
`proximo_control`, editables ahí mismo, sin haber escrito ninguna vista para
eso.

---

## Paso 7 — Exponer la relación N:M con `TabularInline` (Ejercicio 7)

```python
class ConsumoInsumoInline(admin.TabularInline):
    model = ConsumoInsumo
    extra = 1
```

Para la relación muchos a muchos se usó `TabularInline` en lugar de
`StackedInline`, porque aquí puede haber **varias filas** (varios insumos
consumidos en la misma cita), y una tabla se lee mejor que varios bloques
apilados. Dentro de la pantalla de Cita apareció la tabla "Consumos de
insumos" con las columnas `Insumo`, `Cantidad` y `Precio unitario` — que son
justamente los atributos propios del modelo intermedio `ConsumoInsumo`, no
de `Cita` ni de `Insumo` por separado — editables fila por fila, con un botón
para agregar una fila más.

---

## Paso 8 — Probar el flujo completo y sacar la conclusión pedida (Ejercicio 8)

Con todo ya registrado y personalizado, se hizo una prueba real de extremo a
extremo: sobre la cita "Michi" (Ana Torres, Vacunación) se completó por
primera vez su Ficha Clínica (peso 4.2 kg, diagnóstico "Sano, aplicada vacuna
antirrábica") usando el `StackedInline`, y se confirmó que el consumo de
insumo que ya tenía cargado (una jeringa de 5 ml) se mantuvo intacto al
guardar, gracias al `TabularInline`. El Admin devolvió el mensaje de
confirmación de siempre y el listado reflejó el cambio de inmediato — el
mismo patrón de Post/Redirect/Get que ya se había visto en semanas
anteriores, solo que aquí lo generó Django automáticamente, sin que se
escribiera una sola línea en `views.py` ni en `urls.py` para esta pantalla.

Esto lleva directo a la pregunta que pide el ejercicio: **¿qué resuelve el
Admin y qué seguiría necesitando una View y un Template propios?** El Admin
resolvió, sin escribir código de presentación, el CRUD completo de `Cita` y
de sus dos relaciones (la 1:1 vía Inline apilado, la N:M vía Inline
tabular), reutilizando el mismo Model y el mismo ORM que ya existían desde
semanas atrás. Pero el Admin está pensado para el **staff** — quien
administra el sistema — no para el cliente final. No sirve, por ejemplo,
para que el dueño de una mascota reserve su propia cita desde una pantalla
pública, no controla cómo se ve esa pantalla para ese usuario, y no aplica
reglas de negocio propias del flujo público, como la validación que evita
que dos citas se crucen en el mismo horario, que ya existía en la vista de
creación construida en laboratorios anteriores. Para eso sigue haciendo
falta la View y el Template propios de `vet`, que conviven sin problema con
el Admin dentro del mismo proyecto.

---

## Cómo se verificó cada paso (resumen de pruebas)

| Paso | Qué se probó | Resultado |
|---|---|---|
| 1 | `showmigrations vet` muestra las dos migraciones aplicadas | Correcto |
| 2 | Login con el superusuario redirige al panel del Admin | Correcto |
| 3 | Aparecen Citas, Insumos y Veterinarios en el panel | Correcto |
| 4 | Buscar una cita por mascota/dueño filtra el listado | Correcto |
| 5 | Filtrar por estado, servicio o fecha reduce el listado | Correcto |
| 6 | Abrir una Cita muestra el Inline de Ficha Clínica | Correcto |
| 7 | Abrir una Cita con consumos muestra el Inline con filas editables | Correcto |
| 8 | Completar la Ficha Clínica y guardar conserva los consumos ya cargados | Correcto |

---

## Conclusión de la Parte 1

El hilo conductor de estos ocho pasos es que **nada de esto tocó
`models.py`**: las tres relaciones ya estaban bien diseñadas desde la Semana
4, y todo lo que hizo el Laboratorio 5 fue decidir cómo mostrarlas y
administrarlas — qué se registra como listado propio (`Cita`, `Veterinario`,
`Insumo`) y qué se expone únicamente como parte de otra pantalla mediante
Inlines (`FichaClinica`, `ConsumoInsumo`), qué columnas y filtros tiene
sentido ofrecerle a quien administra el sistema, y cómo comprobar que todo
eso funciona de verdad contra datos reales, no solo leyendo el código.

> **Nota aparte:** al probar el Ejercicio 8 se notó que el campo `Servicio`
> de la cita "Michi" llegaba vacío en el formulario, por un problema de
> codificación de texto heredado de un script de carga de datos de semanas
> anteriores (`VacunaciÃ³n` en vez de `Vacunación`). Se corrigió esa fila a
> mano; no es un problema del Django Admin ni forma parte del alcance de
> este laboratorio, pero se deja anotado por transparencia.
