from biblioteca.models import Categoria, Libro
from biblioteca.serializers import LibroSerializer

print('--- Un libro serializado ---')
print(LibroSerializer(Libro.objects.first()).data)

print('--- Varios libros (many=True) ---')
print(LibroSerializer(Libro.objects.all(), many=True).data)

Libro.objects.filter(isbn='978-API-0001').delete()
categoria = Categoria.objects.first()

print('--- Caso valido ---')
valido = LibroSerializer(data={
    'titulo': 'Libro de prueba API',
    'autor': 'Autor Prueba',
    'isbn': '978-API-0001',
    'anio_publicacion': 2020,
    'copias': 2,
    'categoria': categoria.pk,
})
print('is_valid:', valido.is_valid())
print('validated_data:', valido.validated_data)
print('errors:', valido.errors)
print('guardado:', valido.save())

print('--- Caso invalido (año 1200) ---')
invalido = LibroSerializer(data={
    'titulo': 'Libro invalido',
    'autor': 'Autor Prueba',
    'isbn': '978-API-0002',
    'anio_publicacion': 1200,
    'copias': 2,
    'categoria': categoria.pk,
})
print('is_valid:', invalido.is_valid())
print('errors:', invalido.errors)