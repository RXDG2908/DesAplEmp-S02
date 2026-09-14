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
    """Semana 4: deja de ser independiente. Ahora se relaciona con Libro en
    muchos a muchos a traves del modelo intermedio Prestamo (criterio 4)."""
    nombre = models.CharField(max_length=100)
    dni = models.CharField('DNI', max_length=15, unique=True)
    telefono = models.CharField(max_length=20, blank=True)

    # --- N:M con modelo intermedio (criterio 4) ---
    libros = models.ManyToManyField(
        'Libro',
        through='Prestamo',
        related_name='socios',
        blank=True,
    )

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


class CarnetSocio(models.Model):
    """UNO A UNO (criterio 3): credencial fisica del socio.

    No son "mas campos de Socio" porque el carnet tiene ciclo de vida propio:
    se emite, vence, se renueva, se pierde y se reemplaza. Un socio recien
    inscrito todavia no tiene carnet emitido.
    CASCADE: el carnet no tiene existencia propia sin su socio.
    """
    socio = models.OneToOneField(
        Socio,
        on_delete=models.CASCADE,
        related_name='carnet',
    )
    codigo = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    vigente = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Carnet de socio'
        verbose_name_plural = 'Carnets de socios'

    def __str__(self):
        return f'Carnet {self.codigo} - {self.socio.nombre}'


class Prestamo(models.Model):
    """Modelo intermedio (through) de Socio <-> Libro.

    Sus cuatro atributos pertenecen a la RELACION, no a las entidades: existen
    solo porque ese socio se llevo ese ejemplar ese dia.
    PROTECT en ambas FK: el historial de prestamos es un registro contable de
    la biblioteca; no se puede borrar un socio ni un libro con prestamos.
    NOTA: a proposito NO se pone unique_together(socio, libro): la relacion es
    temporal y el mismo socio puede pedir el mismo libro varias veces.
    """
    ESTADOS = [
        ('Activo', 'Activo'),
        ('Devuelto', 'Devuelto'),
        ('Atrasado', 'Atrasado'),
        ('Extraviado', 'Extraviado'),
    ]

    socio = models.ForeignKey(Socio, on_delete=models.PROTECT,
                              related_name='prestamos')
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT,
                              related_name='prestamos')
    fecha_prestamo = models.DateField()
    fecha_devolucion_prevista = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='Activo')

    class Meta:
        ordering = ['-fecha_prestamo']
        verbose_name_plural = 'Préstamos'

    def __str__(self):
        return f'{self.libro.titulo} -> {self.socio.nombre} ({self.fecha_prestamo})'
