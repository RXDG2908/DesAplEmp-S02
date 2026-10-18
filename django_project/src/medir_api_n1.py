# Laboratorio 08 - Ejercicio 7: consultas que ejecuta la serializacion
# anidada de TODAS las citas, antes y despues de optimizar el queryset.
# Uso:  python manage.py shell -c "exec(open('medir_api_n1.py', encoding='utf-8').read())"
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext

from vet.models import Cita
from vet.serializers import CitaSerializer

# connection.queries solo se llena con DEBUG=True; CaptureQueriesContext
# fuerza el registro para que la medicion no dependa de settings.
with CaptureQueriesContext(connection):
    reset_queries()
    CitaSerializer(Cita.objects.all(), many=True).data
    antes = len(connection.queries)

    reset_queries()
    optimizado = (Cita.objects
                  .select_related('veterinario', 'ficha')
                  .prefetch_related('consumos__insumo'))
    CitaSerializer(optimizado, many=True).data
    despues = len(connection.queries)

print('Citas serializadas:', Cita.objects.count())
print('Consultas SIN optimizar (Cita.objects.all()):', antes)
print('Consultas CON select_related + prefetch_related:', despues)
