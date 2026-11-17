# ==================================================================
# GUIA: ARCHIVO  medir_api_n1_bib.py  (script de medicion)
# LAB     : 08 Parte 2 (biblioteca)
# QUE HACE : mide las consultas de PrestamoSerializer antes y despues de optimizar.
# ==================================================================
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext

from biblioteca.models import Prestamo
from biblioteca.serializers import PrestamoSerializer

with CaptureQueriesContext(connection):
    reset_queries()
    PrestamoSerializer(Prestamo.objects.all(), many=True).data
    antes = len(connection.queries)

    reset_queries()
    optimizado = Prestamo.objects.select_related('socio', 'libro')
    PrestamoSerializer(optimizado, many=True).data
    despues = len(connection.queries)

print('Prestamos serializados:', Prestamo.objects.count())
print('Consultas SIN optimizar (Prestamo.objects.all()):', antes)
print('Consultas CON select_related:', despues)