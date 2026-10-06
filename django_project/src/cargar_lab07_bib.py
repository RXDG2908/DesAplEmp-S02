from datetime import date, timedelta
from biblioteca.models import Categoria, Libro, Socio, Prestamo

cat_nov, _ = Categoria.objects.get_or_create(nombre='Novela', defaults={'descripcion': 'Narrativa de ficción'})
cat_his, _ = Categoria.objects.get_or_create(nombre='Historia', defaults={'descripcion': 'Ensayo histórico'})
cat_cie, _ = Categoria.objects.get_or_create(nombre='Ciencia', defaults={'descripcion': 'Divulgación científica'})

datos_libros = [
    ('La ciudad y los perros', 'M. Vargas Llosa', '9788420471839', 1963, cat_nov, 5),
    ('Los ríos profundos', 'J. M. Arguedas', '9788437604350', 1958, cat_nov, 4),
    ('Historia de la República', 'J. Basadre', '9786124161070', 1939, cat_his, 3),
    ('Cosmos', 'Carl Sagan', '9780345539434', 1980, cat_cie, 6),
    ('Breve historia del tiempo', 'Stephen Hawking', '9788498929355', 1988, cat_cie, 2),
]
libros = []
for t, a, i, y, c, n in datos_libros:
    l, _ = Libro.objects.get_or_create(isbn=i, defaults=dict(titulo=t, autor=a, anio_publicacion=y, categoria=c, copias=n))
    libros.append(l)

datos_socios = [('Carlos Ramos', '70123456'), ('Elena Vega', '71998877'), ('Diego Salas', '72345610'), ('Rosa Medina', '73456721')]
socios = [Socio.objects.get_or_create(dni=d, defaults=dict(nombre=n))[0] for n, d in datos_socios]

hoy = date.today()
prestamos = [
    (0, 0, -3, 'Activo', '0'),
    (0, 2, -30, 'Devuelto', '0'),
    (1, 1, -20, 'Atrasado', '5.00'),
    (1, 3, -5, 'Activo', '0'),
    (2, 3, -40, 'Devuelto', '2.50'),
    (2, 4, -18, 'Atrasado', '7.50'),
    (3, 0, -8, 'Activo', '0'),
    (3, 2, -25, 'Extraviado', '30.00'),
    (0, 4, -2, 'Activo', '0'),
]
for si, li, dias, estado, multa in prestamos:
    f = hoy + timedelta(days=dias)
    Prestamo.objects.get_or_create(
        socio=socios[si], libro=libros[li], fecha_prestamo=f,
        defaults=dict(fecha_devolucion_prevista=f + timedelta(days=14), estado=estado, multa=multa),
    )

print(Libro.objects.count(), Socio.objects.count(), Prestamo.objects.count(), Categoria.objects.count())