# ==================================================================
# GUIA: ARCHIVO  medir_n1.py  (script de medicion)
# LAB     : 07 Parte 1 (vet)  -  EJERCICIO: Ej.8 problema N+1
# QUE HACE : cuenta las consultas SQL con y sin select_related / prefetch_related (6 -> 1 y 15 -> 3).
# USO     : python ./manage.py shell -c "exec(open('medir_n1.py', encoding='utf-8').read())"
# DOCS    : ../../docs/guiones/GUION-Lab07-Parte1.md
# ==================================================================
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