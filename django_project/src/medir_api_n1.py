# ==================================================================
# ARCHIVO  : medir_api_n1.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : SCRIPT DE MEDICIÓN de consultas SQL de la API.
# ------------------------------------------------------------------
# LAB 8 - EJ 7: CUENTA las consultas que ejecuta la SERIALIZACIÓN ANIDADA de
#               TODAS las citas, ANTES y DESPUÉS de optimizar (24 -> 3 consultas).
# ------------------------------------------------------------------
# USO      : python ./manage.py shell -c "exec(open('medir_api_n1.py', encoding='utf-8').read())"
# DOCS     : ../../docs/guiones/GUION-Lab08-Parte1.md
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 8 - EJ 7 ..... línea 23
# ==================================================================
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext

from vet.models import Cita
from vet.serializers import CitaSerializer

# connection.queries SOLO se llena con DEBUG=True; CaptureQueriesContext
# FUERZA el registro para que la medición no dependa de settings.py.
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
