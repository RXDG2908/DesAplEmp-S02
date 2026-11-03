# Guión expositivo — Laboratorio 5, Parte 1 (Veterinaria)

Guión para exponer en voz alta lo que se hizo en la parte del laboratorio
correspondiente a la aplicación de la veterinaria, indicando en qué archivo
está cada cosa.

## Introducción

"En esta parte del laboratorio no se creó ninguna entidad nueva. Todo lo
que se trabajó está en un único archivo: `vet/admin.py`. Ahí se registró y
se personalizó, dentro del panel de administración de Django, lo que ya
existía desde la semana anterior: las citas, los veterinarios, los
insumos y sus relaciones."

## 1. Registro básico de las entidades

"Al final del archivo `vet/admin.py` están las tres líneas de registro:
`admin.site.register(Cita, CitaAdmin)`, `admin.site.register(Veterinario,
VeterinarioAdmin)` y `admin.site.register(Insumo)`. Estas tres líneas son
las que hacen que Cita, Veterinario e Insumo aparezcan en el panel de
administración. Insumo se registró de forma simple, sin personalización,
porque no lo necesitaba; Cita y Veterinario sí llevan una clase propia que
los personaliza."

## 2. Personalización de la lista de citas

"La personalización de Cita está en la clase `CitaAdmin`, dentro del mismo
archivo `vet/admin.py`. Ahí se definieron tres cosas: `list_display`, que
son las columnas que se muestran en la lista, y que en este caso son
mascota, dueño, servicio, fecha, hora, estado y veterinario; `search_fields`,
que permite buscar por mascota o por dueño; y `list_filter`, que agrega
filtros por estado, por servicio y por fecha."

## 3. Personalización de la lista de veterinarios

"De la misma forma, la clase `VeterinarioAdmin`, también en `vet/admin.py`,
define `list_display` con nombre, colegiatura y especialidad, y
`search_fields` para buscar por nombre o por colegiatura."

## 4. La relación uno a uno: ficha clínica

"Arriba de `CitaAdmin`, en el mismo archivo, está la clase
`FichaClinicaInline`, que hereda de `admin.StackedInline`. Esta clase es la
que hace que la ficha clínica de una cita aparezca integrada, como un
bloque, dentro de la misma pantalla de esa cita. Se usó `StackedInline` y
no la otra opción porque la relación entre Cita y FichaClinica es de uno a
uno: como máximo hay una ficha por cita, así que tiene sentido mostrarla
como un bloque único en vez de como una tabla de varias filas."

## 5. La relación de muchos a muchos: consumo de insumos

"Justo debajo está la clase `ConsumoInsumoInline`, que hereda de
`admin.TabularInline`. Esta controla cómo se muestra el consumo de
insumos dentro de la cita. Aquí sí se usó `TabularInline`, que muestra los
datos como una tabla con una fila por cada insumo usado, porque la
relación entre Cita e Insumo es de muchos a muchos, con un dato propio de
cantidad y precio unitario en cada fila."

## 6. Cómo se conectan los inlines a la cita

"Estas dos clases, `FichaClinicaInline` y `ConsumoInsumoInline`, no hacen
nada por sí solas: se activan dentro de `CitaAdmin` mediante la línea
`inlines = [FichaClinicaInline, ConsumoInsumoInline]`. Esa línea es la que
hace que, al abrir una cita en el panel, aparezcan debajo la ficha clínica
y la tabla de insumos consumidos, sin necesidad de salir de esa pantalla."

## 7. Verificación

"La verificación no se hizo leyendo el código, sino usando el navegador:
se entró al panel de administración, se inició sesión, se revisó la lista
de citas con sus columnas, su buscador y sus filtros, se comprobó que la
ficha clínica y los insumos aparecieran dentro de la cita como bloques
integrados, y se hizo una edición real sobre una cita para confirmar que
el guardado funcionaba correctamente contra la base de datos."

## Cierre

"En resumen, todo el trabajo de esta parte vive en un solo archivo,
`vet/admin.py`: dos clases inline para las relaciones uno a uno y muchos a
muchos, dos clases ModelAdmin para personalizar las listas de Cita y
Veterinario, y tres líneas de registro que conectan todo con el panel de
administración de Django."
