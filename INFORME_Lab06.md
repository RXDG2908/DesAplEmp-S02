# Informe — Laboratorio 06: Motor de plantillas de Django

**Curso:** Desarrollo de Aplicaciones Empresariales — 4 - C24 - Sección CD
**Estudiantes:** Lucas Inga - Renzo Leon

En este laboratorio no se crearon vistas ni plantillas nuevas: se revisaron y
ajustaron las que ya existían en las dos aplicaciones del equipo, vet
(Parte 1) y biblioteca (Parte 2). Las rutas, las vistas y los modelos no
cambiaron.

## PARTE 1 — Refactorizar los templates de vet

### Ejercicio 1 — Auditar los templates actuales

Se revisaron las tres plantillas de vet: el listado de citas, el formulario
para registrar una cita y el detalle de una cita. Las tres ya heredaban de la
plantilla base desde semanas anteriores, así que no había ninguna que migrar
desde cero.

### Ejercicio 2 — Crear la plantilla base

La plantilla base ya existía. Tiene el encabezado con el título, el menú de
navegación con los enlaces a citas, libros, socios, préstamos y carnets, un
pie de página, y un espacio vacío llamado contenido donde cada plantilla hija
pone lo suyo. En este laboratorio solo se cambió el texto del pie de página
para que diga Laboratorio 06.

### Ejercicio 3 — Migrar un template a herencia

El listado de citas empieza indicando que hereda de la plantilla base y
define solo su contenido dentro del espacio correspondiente. La vista que lo
muestra no se tocó y la página sigue mostrando los mismos datos.

### Ejercicio 4 — Migrar el resto de los templates

El formulario de nueva cita y el detalle de cita usan la misma plantilla base
y solo escriben su parte. Con esto las tres plantillas de vet comparten el
mismo encabezado, menú y pie.

### Ejercicio 5 — Aplicar un filtro

Ya se usaban filtros para dar formato a las fechas y las horas, para contar
las citas del listado y para mostrar un texto por defecto cuando falta un
dato. En este laboratorio se agregaron dos más: los precios y subtotales de
los insumos en el detalle de la cita se muestran siempre con dos decimales, y
el nombre de la mascota en el listado se muestra con la primera letra de cada
palabra en mayúscula.

### Ejercicio 6 — Documentar con comentarios

Las plantillas de vet tienen comentarios que no se ven en la página final.
Por ejemplo, en el detalle de cita hay uno antes de cada una de las tres
relaciones explicando qué tipo de acceso se está usando, y en el listado hay
uno que aclara que el veterinario se obtiene sin consultas extra.

### Ejercicio 7 — Reutilizar con include

El nombre del veterinario junto con su especialidad se mostraba igual en el
listado y en el detalle. Ese fragmento se pasó a un archivo aparte y ambas
plantillas lo insertan con la etiqueta de inclusión. Si mañana cambia cómo se
muestra el veterinario, se edita en un solo lugar.

### Ejercicio 8 — Seguridad y comparación con el Admin

Se registró una cita con el nombre de mascota escrito como una etiqueta de
script y el dueño con etiquetas de negrita. Al abrir el listado, el texto se
ve tal cual, como letras, y el código fuente de la página muestra los signos
menor y mayor convertidos en sus entidades seguras. El script nunca se
ejecutó. Django hace esto solo con cada dato que se muestra entre llaves
dobles.

Lo que gana la aplicación frente al Admin: el Admin es una herramienta
interna para el personal, que solo entra con usuario y contraseña. Las
plantillas propias en cambio arman las páginas públicas que ve el cliente,
con el diseño de la clínica, sus propias direcciones y datos ordenados como
conviene, todo con una estructura común que se cambia en un solo sitio y con
el escape automático protegiendo cada campo.

**Casos de prueba**

| # | Caso | Resultado esperado | Resultado obtenido |
|---|------|--------------------|--------------------|
| 1 | Abrir el listado de citas | Se muestra con menú y pie de la base | Correcto |
| 2 | Abrir el detalle de una cita | Las tres relaciones se muestran igual que antes | Correcto |
| 3 | Precios de insumos | Siempre con dos decimales | Correcto |
| 4 | Registrar una cita con un script en el nombre | Se muestra como texto, no se ejecuta | Correcto |
| 5 | Registrar una cita normal | Aparece en el listado | Correcto |

## PARTE 2 — Refactorizar los templates de biblioteca

### Ejercicio 9 — Auditar los templates de la investigación propia

Las siete entidades tienen pantalla propia: libros, categorías,
editoriales, bibliotecarios, socios, carnets y préstamos, además del detalle
de socio. Todas ya heredaban de la plantilla base. Se eligieron para el
trabajo de este laboratorio el listado de préstamos y el detalle de socio,
que son los que muestran la relación de muchos a muchos.

**Lista de comprobación**

| # | Criterio | Estado |
|---|----------|--------|
| 1 | Al menos dos templates heredan de la base | Cumple, todos heredan |
| 2 | La pantalla con relación sigue igual | Cumple, el detalle de socio muestra carnet y préstamos |
| 3 | Al menos un filtro | Cumple, fechas, sí o no, texto por defecto |
| 4 | Al menos un comentario | Cumple, hay en varios templates |
| 5 | Al menos un include entre dos templates | Cumple, fragmento de préstamo |
| 6 | El CRUD sigue funcionando | Cumple |
| 7 | Prueba con un script en un formulario | Cumple, ver ejercicio 12 |
| 8 | Ninguna pantalla depende del Admin | Cumple, las direcciones son las públicas |
| 9 | Explicación frente al Admin | Ver ejercicio 13 |

### Ejercicio 10 — Migrar el resto de los templates

Los formularios y las pantallas de confirmación de borrado de biblioteca son
plantillas genéricas que también heredan de la base. No quedó ninguna
plantilla sin herencia.

### Ejercicio 11 — Reutilizar con include en biblioteca

Las columnas de fecha de préstamo, fecha prevista de devolución, fecha real y
estado se repetían en el listado de préstamos y en el detalle de socio. Se
sacaron a un fragmento aparte que ambas plantillas insertan, pasándole el
préstamo que corresponde a cada fila.

### Ejercicio 12 — Verificar seguridad en un formulario existente

Se aplicó la misma prueba del ejercicio 8. Como todas las plantillas de
biblioteca muestran los datos con llaves dobles y ninguna usa el filtro que
desactiva el escape, el resultado es el mismo: el texto se ve como letras y
no se ejecuta.

### Ejercicio 13 — Verificar el flujo completo

Se recorrieron el listado de citas, el detalle de cita, el listado de
préstamos y el detalle de socio con los datos de prueba del proyecto. Todas
las páginas cargan bien y muestran la misma información que antes de la
refactorización. Frente al Admin, que sirve para que el personal cargue y
corrija datos rápido, las pantallas propias son las que ve el usuario final y
las que se pueden ordenar y reutilizar a gusto.

### Ejercicio 14 — Publicar en GitHub

El README quedó actualizado con las plantillas tocadas en este laboratorio
y el archivo de requisitos no cambió, porque no se instaló nada nuevo.
Repositorio: https://github.com/RXDG2908/DesAplEmp-S02

## Conclusiones

- Cambiar de una plantilla que repite todo a una que hereda de la base no
  cambia lo que ve el usuario, pero deja el mantenimiento en un solo lugar.
- Los filtros permiten dar formato a los datos sin tocar las vistas.
- La inclusión de fragmentos evita copiar y pegar el mismo pedazo de página
  en varias plantillas.
- El escape automático protege los datos escritos por los usuarios sin que
  haya que programar nada extra.
- El Admin y las plantillas propias se complementan: uno es para el personal
  interno y las otras para el cliente.
