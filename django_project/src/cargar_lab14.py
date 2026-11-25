# ==================================================================
# ARCHIVO  : cargar_lab14.py
# PARTE 1 y PROYECTO : CAFETERÍA (catálogo y pedidos) y CHAMBA PE (rubros, clientes, solicitudes)
# ROL      : SCRIPT DE DATOS DE PRUEBA. Se puede correr varias veces (borra y vuelve a crear).
# ------------------------------------------------------------------
# LAB 14 - EJ 3 : 2 categorías y 5 productos de la cafetería con Producto.objects.create(...).
# LAB 14 - EJ 4 : un cliente de la cafetería para los pedidos.
# LAB 14 - EJ 10: rubros, 4 clientes y 3 solicitudes de Chamba PE con su seguimiento.
# ------------------------------------------------------------------
# USO      : python manage.py shell < cargar_lab14.py
#            (antes: python manage.py shell < cargar_chamba.py para tener los prestadores)
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 3 .... línea 31
#   LAB 14 - EJ 4 .... línea 38
#   LAB 14 - EJ 10 ... línea 46
# ==================================================================
from catalogo.models import Categoria, Producto
from chamba.models import Prestador
from clientes.models import Cliente
from pedidos.models import Cliente as ClienteTienda, Pedido
from servicios.models import Rubro
from solicitudes.models import SeguimientoSolicitud, Solicitud

# ---------- PARTE 1: cafetería ----------
Pedido.objects.all().delete()
Producto.objects.all().delete()
Categoria.objects.all().delete()
ClienteTienda.objects.all().delete()

bebidas = Categoria.objects.create(nombre='Bebidas')
postres = Categoria.objects.create(nombre='Postres')
Producto.objects.create(categoria=bebidas, nombre='Café americano', precio='6.50', stock=50)
Producto.objects.create(categoria=bebidas, nombre='Capuchino', precio='9.00', stock=40)
Producto.objects.create(categoria=bebidas, nombre='Jugo de naranja', precio='7.00', stock=0)
Producto.objects.create(categoria=postres, nombre='Torta de chocolate', precio='10.50', stock=5)
Producto.objects.create(categoria=postres, nombre='Tostada', precio='4.50', stock=10)
ClienteTienda.objects.create(nombre='Ana Torres', email='ana.torres@correo.pe')
print('Productos:', list(Producto.objects.all()))

# ---------- PARTE 2: Chamba PE ----------
Solicitud.objects.all().delete()
Cliente.objects.all().delete()
Rubro.objects.all().delete()

rubros = {n: Rubro.objects.create(nombre=n, descripcion=d) for n, d in [
    ('Gasfitería', 'Tuberías, caños y desagües'),
    ('Electricidad', 'Cortocircuitos, tomacorrientes e instalaciones'),
    ('Costura', 'Arreglos de ropa al momento'),
    ('Carpintería', 'Puertas, muebles y chapas'),
    ('Primeros auxilios', 'Atención básica a domicilio'),
]}
c1 = Cliente.objects.create(nombres='Lucía', apellidos='Quispe Rojas', telefono='987654321', email='lucia.quispe@correo.pe')
c2 = Cliente.objects.create(nombres='Marco', apellidos='Vela Sánchez', telefono='912345678', email='marco.vela@correo.pe')
c3 = Cliente.objects.create(nombres='Elena', apellidos='Ruiz Paredes', telefono='956781234', email='elena.ruiz@correo.pe')
Cliente.objects.create(nombres='Jorge', apellidos='Linares Soto', telefono='934567812', email='jorge.linares@correo.pe')

carlos = Prestador.objects.get(nombres='Carlos')   # Gasfitería, Aprobado, S/ 60
rosa = Prestador.objects.get(nombres='Rosa')       # Electricidad, Aprobado, S/ 55
luis = Prestador.objects.get(nombres='Luis')       # Electricidad, Aprobado, S/ 50


def crear(cliente, prestador, direccion, descripcion, avances):
    s = Solicitud.objects.create(cliente=cliente, prestador=prestador, rubro=rubros[prestador.rubro],
                                 direccion=direccion, descripcion=descripcion, monto=prestador.tarifa)
    SeguimientoSolicitud.objects.create(solicitud=s, estado='PEN', nota='Solicitud creada por el cliente')
    for estado in avances:
        s.estado = estado
        s.save()
        SeguimientoSolicitud.objects.create(solicitud=s, estado=estado)
    return s


crear(c1, carlos, 'Av. Los Olivos 345, San Martín de Porres', 'Se rompió la tubería del baño', ['CON', 'CAM', 'SER', 'FIN', 'PAG'])
crear(c2, rosa, 'Jr. Huallaga 120, Cercado de Lima', 'Corto circuito en la cocina', ['CON'])
crear(c3, luis, 'Calle Las Begonias 78, San Isidro', 'Instalar dos tomacorrientes', [])
print('Rubros:', Rubro.objects.count(), '| Clientes:', Cliente.objects.count(),
      '| Solicitudes:', Solicitud.objects.count(), '| Seguimientos:', SeguimientoSolicitud.objects.count())
