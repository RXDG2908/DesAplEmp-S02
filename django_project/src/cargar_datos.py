"""Datos de prueba para las capturas del Laboratorio 04.

Uso:  python manage.py shell < cargar_datos.py
"""
from datetime import date, time, timedelta

from vet.models import Cita, ConsumoInsumo, FichaClinica, Insumo, Veterinario
from biblioteca.models import (CarnetSocio, Categoria, Editorial, Libro,
                               Bibliotecario, Prestamo, Socio)

# ---------- App vet ----------
v1 = Veterinario.objects.create(nombre='Dra. Karla Ruiz', colegiatura='CMVP-4821',
                                especialidad='Cirugía menor')
v2 = Veterinario.objects.create(nombre='Dr. Mario Salas', colegiatura='CMVP-3907',
                                especialidad='Medicina interna')

c1 = Cita.objects.create(mascota='Rocky', dueno='Luis Pérez', servicio='Cirugía',
                         fecha=date(2026, 3, 10), hora=time(10, 30),
                         estado='Atendida', veterinario=v1)
c2 = Cita.objects.create(mascota='Michi', dueno='Ana Torres', servicio='Vacunación',
                         fecha=date(2026, 3, 11), hora=time(9, 0),
                         estado='Confirmada', veterinario=v2)

FichaClinica.objects.create(cita=c1, peso_kg=12.40,
                            diagnostico='Absceso en pata trasera derecha.',
                            tratamiento='Drenaje + antibiótico por 7 días.',
                            proximo_control=date(2026, 3, 17))

jer = Insumo.objects.create(nombre='Jeringa 5ml', stock=100)
ant = Insumo.objects.create(nombre='Antibiótico inyectable', unidad='ampolla', stock=30)
gas = Insumo.objects.create(nombre='Gasa estéril', unidad='paquete', stock=45)

ConsumoInsumo.objects.create(cita=c1, insumo=jer, cantidad=2, precio_unitario=1.50)
ConsumoInsumo.objects.create(cita=c1, insumo=ant, cantidad=1, precio_unitario=18.00)
ConsumoInsumo.objects.create(cita=c1, insumo=gas, cantidad=3, precio_unitario=2.50)
ConsumoInsumo.objects.create(cita=c2, insumo=jer, cantidad=1, precio_unitario=1.50)

# ---------- App biblioteca ----------
Bibliotecario.objects.create(nombre='Rosa Quispe', dni='45120398', turno='Mañana')
Editorial.objects.create(nombre='Alfaguara', pais='España')

cat1 = Categoria.objects.create(nombre='Novela', descripcion='Narrativa de ficción')
cat2 = Categoria.objects.create(nombre='Historia', descripcion='Ensayo histórico')

l1 = Libro.objects.create(titulo='La ciudad y los perros', autor='M. Vargas Llosa',
                          isbn='9788420471839', anio_publicacion=1963, categoria=cat1)
l2 = Libro.objects.create(titulo='Los ríos profundos', autor='J. M. Arguedas',
                          isbn='9788437604350', anio_publicacion=1958, categoria=cat1)
l3 = Libro.objects.create(titulo='Historia de la República', autor='J. Basadre',
                          isbn='9786124161070', anio_publicacion=1939, categoria=cat2)

s1 = Socio.objects.create(nombre='Carlos Ramos', dni='70123456', telefono='987654321')
s2 = Socio.objects.create(nombre='Elena Vega', dni='71998877', telefono='912345678')

CarnetSocio.objects.create(socio=s1, codigo='BIB-0001',
                           fecha_emision=date(2026, 1, 15),
                           fecha_vencimiento=date(2027, 1, 15), vigente=True)
# s2 queda a proposito SIN carnet: demuestra que el 1:1 es opcional.

hoy = date(2026, 3, 1)
Prestamo.objects.create(socio=s1, libro=l1, fecha_prestamo=hoy,
                        fecha_devolucion_prevista=hoy + timedelta(days=14),
                        estado='Activo')
Prestamo.objects.create(socio=s1, libro=l3, fecha_prestamo=date(2026, 1, 20),
                        fecha_devolucion_prevista=date(2026, 2, 3),
                        fecha_devolucion_real=date(2026, 2, 1), estado='Devuelto')
Prestamo.objects.create(socio=s2, libro=l2, fecha_prestamo=date(2026, 2, 10),
                        fecha_devolucion_prevista=date(2026, 2, 24),
                        estado='Atrasado')
# El mismo socio puede pedir el mismo libro otra vez (por eso NO hay unique).
Prestamo.objects.create(socio=s1, libro=l1, fecha_prestamo=date(2025, 11, 5),
                        fecha_devolucion_prevista=date(2025, 11, 19),
                        fecha_devolucion_real=date(2025, 11, 18), estado='Devuelto')

print('Datos de prueba cargados.')
