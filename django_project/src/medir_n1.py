# ==================================================================
# ARCHIVO  : medir_n1.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : SCRIPT DE MEDICIÓN de consultas SQL.
# ------------------------------------------------------------------
# LAB 7 - EJ 8: MIDE el PROBLEMA N+1 con connection.queries y reset_queries:
#               veterinario  SIN vs CON select_related   (6 -> 1 consulta)
#               consumos     SIN vs CON prefetch_related (15 -> 3 consultas)
# ------------------------------------------------------------------
# USO      : python ./manage.py shell -c "exec(open('medir_n1.py', encoding='utf-8').read())"
# DOCS     : ../../docs/guiones/GUION-Lab07-Parte1.md
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 7 - EJ 8 ..... línea 19
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