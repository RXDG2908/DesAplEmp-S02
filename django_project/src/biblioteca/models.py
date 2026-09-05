# biblioteca/models.py
# Problemática (Ejercicio 7): una biblioteca comunitaria de barrio lleva su
# catálogo de libros y el registro de socios y bibliotecarios en cuadernos y
# hojas de cálculo sueltas. No hay forma centralizada de saber qué libros
# existen, de qué categoría son ni quién los administra. Esta App resuelve
# ese registro central mediante Django ORM y SQLite.
#
# Ejercicio 9 — Modelo de datos: cinco entidades.
#   - Tres INDEPENDIENTES (no se relacionan entre sí ni con otra entidad):
#     Bibliotecario, Editorial, Socio.
#   - Dos RELACIONADAS mediante ForeignKey: Categoria (lado "1") y
#     Libro (lado "N", cada libro pertenece a una sola categoría).

from django.db import models


class Bibliotecario(models.Model):
    """Entidad independiente: persona encargada de administrar el catálogo."""
    TURNOS = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
    ]

    nombre = models.CharField(max_length=100)
    dni = models.CharField('DNI', max_length=15, unique=True)
    turno = models.CharField(max_length=10, choices=TURNOS)

    def __str__(self):
        return f'{self.nombre} ({self.turno})'


class Editorial(models.Model):
    """Entidad independiente: casa editorial."""
    nombre = models.CharField(max_length=100)
    pais = models.CharField('País de origen', max_length=60)

    def __str__(self):
        return self.nombre


class Socio(models.Model):
    """Entidad independiente: persona registrada como socia de la biblioteca."""
    nombre = models.CharField(max_length=100)
    dni = models.CharField('DNI', max_length=15, unique=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    """Lado '1' de la relación ForeignKey (Ejercicio 9 y 10)."""
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    """Lado 'N' de la relación ForeignKey: cada Libro pertenece a UNA
    Categoria, pero una Categoria puede tener MUCHOS libros (1 a N)."""
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    isbn = models.CharField('ISBN', max_length=20, unique=True)
    anio_publicacion = models.PositiveIntegerField('Año de publicación')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='libros',
    )

    def __str__(self):
        return f'{self.titulo} ({self.categoria})'
