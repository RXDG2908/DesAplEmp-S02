from django.db import connection, reset_queries
from biblioteca.models import Libro, Prestamo

reset_queries()
for p in Prestamo.objects.all():
    n = p.socio.nombre + p.libro.titulo
print('Prestamos SIN optimizar:', len(connection.queries))

reset_queries()
for p in Prestamo.objects.select_related('socio', 'libro'):
    n = p.socio.nombre + p.libro.titulo
print('Prestamos CON select_related:', len(connection.queries))

reset_queries()
for l in Libro.objects.all():
    c = l.categoria.nombre
    for p in l.prestamos.all():
        s = p.socio.nombre
print('Libros SIN optimizar:', len(connection.queries))

reset_queries()
for l in Libro.objects.select_related('categoria').prefetch_related('prestamos__socio'):
    c = l.categoria.nombre
    for p in l.prestamos.all():
        s = p.socio.nombre
print('Libros CON select_related + prefetch_related:', len(connection.queries))