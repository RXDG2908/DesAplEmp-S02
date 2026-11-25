# Guión expositivo — Laboratorio 14 (Componentes de la cafetería y de Chamba PE)

## Introducción

"En el laboratorio anterior diseñamos la aplicación y dejamos las apps vacías.
En este laboratorio las llenamos con sus componentes: los modelos y las
migraciones crean las tablas, los serializers y los ViewSets atienden las
solicitudes, el router publica las rutas y React muestra los datos. Además
registramos un pedido con reglas de negocio y un pago simulado. Primero lo hago
con el catálogo de una cafetería y después con la solicitud de servicio de mi
proyecto, Chamba PE."

## Arquitectura: cómo funciona y para qué sirve

"Una solicitud recorre siempre el mismo camino. La pantalla de React pide los
datos con Axios. La ruta, que arma el router, la manda al controlador. En
Django el controlador se llama view: aquí son los ViewSets y las vistas con
reglas. El serializer valida lo que llega y lo convierte a JSON, el modelo lo
guarda con el ORM en SQLite, y la respuesta vuelve con su código.

La regla que más importa es que el servidor decide. Lo explico con un pedido:
React solo manda qué productos y cuántos; Django lee el precio de la base de
datos, descuenta el stock y calcula el total. Si el navegador mandara el
precio, cualquiera podría cambiarlo."

## 1. Modelos, migraciones y relaciones

"En la app catalogo escribí Categoria y Producto: el precio es DecimalField
para no tener errores de redondeo, el stock es PositiveIntegerField para que
la base no acepte negativos, y la categoría es una clave foránea con PROTECT.
Con makemigrations y migrate se crearon las tablas, y en el shell cargué dos
categorías y cinco productos.

En pedidos están Cliente, Pedido, DetallePedido y Pago. Usé PROTECT donde hay
historial: no se borra una categoría con productos, ni un producto vendido, ni
un cliente con pedidos. Usé CASCADE en las líneas del pedido, porque sin su
pedido no tienen sentido. Al intentar borrar la categoría Postres, Django lanzó
ProtectedError."

## 2. Serializer, controlador y rutas

"ProductoSerializer convierte los productos a JSON con el nombre de su
categoría y rechaza con 400 un precio de cero. ProductoViewSet hereda de
ModelViewSet, así que ya sabe listar, crear, ver, editar y eliminar, y tiene
búsqueda. El router genera cinco rutas a partir de dos direcciones:
/api/productos/ para listar y crear, y /api/productos/ con un id para ver,
editar y borrar."

## 3. La vista de React

"ProductosPage pide los productos dentro de un efecto que corre una sola vez y
los dibuja en una tabla con map y key. Mientras espera muestra Cargando, y si
Django está apagado muestra un error. En Network se ve el GET con 200."

## 4. Crear el pedido y pagarlo

"La vista crear_pedido trabaja dentro de una transacción: o se guarda todo, o
nada. Para cada producto descuenta el stock con F, que hace la resta dentro de
la base y solo si alcanza. Si un producto no tiene stock, lanza un error y se
deshace todo, incluso lo que ya había descontado.

Lo probé: con dos capuchinos y un café respondió 201 con un total de 24 soles
con 50, y el stock bajó. Con 99 tortas respondió 400 y el stock quedó igual.
El pago simulado registra el Pago y deja el pedido en Pagado; si intento
pagarlo otra vez, responde 400. En un pago real, React obtiene un token de la
pasarela y Django hace el cobro; nunca guardamos el número de tarjeta."

## 5. Chamba PE: modelos y reglas

"En mi proyecto la entidad principal es la solicitud de servicio. Se relaciona
con el cliente, el prestador y el rubro, las tres con PROTECT para no perder
el historial. Su detalle es el seguimiento: un registro por cada cambio de
estado, con CASCADE.

Las reglas están en el servidor: la dirección debe tener al menos ocho
caracteres, solo un prestador aprobado recibe solicitudes, debe atender ese
rubro y no puede tener otro servicio en curso. Al crear, el monto se toma de
la tarifa guardada: envié un monto de un sol y se guardó 60, que es la tarifa
de Carlos. Y los estados avanzan solo en orden con la acción avanzar. Chamba
PE no maneja stock; la regla equivalente es que un prestador no atienda dos
servicios a la vez."

## 6. Listado, detalle y pago en Chamba PE

"SolicitudesPage lista las solicitudes con carga, error, búsqueda y filtro por
estado. Al pulsar Ver se abre el detalle, que muestra el seguimiento y el
botón para avanzar el estado; la navegación la resolví con estado local. El
pago está descrito en el README: se cobra cuando el servicio queda finalizado,
se envía el token y el monto, la solicitud pasa a pagada, y nunca guardamos
datos de tarjeta. La pasarela real se integra en la Semana 16."

## 7. Cierre

"manage.py check, npm run lint y npm run build terminan sin errores y Django no
dio errores 500. La idea con la que me quedo es que cada componente tiene un
solo trabajo: la base guarda, la ruta dirige, el controlador decide, el
serializer valida y React muestra. Y que el precio, el stock y los estados los
decide siempre el servidor."
