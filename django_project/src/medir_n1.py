from django.db import connection, reset_queries
from vet.models import Cita

reset_queries()
for c in Cita.objects.all():
    nombre = c.veterinario.nombre if c.veterinario else '-'
print('Veterinario SIN optimizar:', len(connection.queries))

reset_queries()
for c in Cita.objects.select_related('veterinario'):
    nombre = c.veterinario.nombre if c.veterinario else '-'
print('Veterinario CON select_related:', len(connection.queries))

reset_queries()
for c in Cita.objects.all():
    for k in c.consumos.all():
        n = k.insumo.nombre
print('Consumos SIN optimizar:', len(connection.queries))

reset_queries()
for c in Cita.objects.prefetch_related('consumos__insumo'):
    for k in c.consumos.all():
        n = k.insumo.nombre
print('Consumos CON prefetch_related:', len(connection.queries))