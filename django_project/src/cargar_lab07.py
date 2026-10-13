# Carga los datos de prueba del Laboratorio 07 (Ejercicio 2).
# Es idempotente: se puede ejecutar varias veces sin duplicar nada.
# Uso:  python manage.py shell -c "exec(open('cargar_lab07.py', encoding='utf-8').read())"
from datetime import date, time

from vet.models import Cita, ConsumoInsumo, Insumo, Veterinario

# Veterinarios (minimo 3): se reutilizan los existentes y se crea el que falte.
v1, _ = Veterinario.objects.get_or_create(
    colegiatura='CMVP-4821', defaults=dict(nombre='Dra. Karla Ruiz', especialidad='Medicina general'))
v2, _ = Veterinario.objects.get_or_create(
    colegiatura='CMVP-3907', defaults=dict(nombre='Dr. Mario Salas', especialidad='Cirugía'))
v3, _ = Veterinario.objects.get_or_create(
    colegiatura='CMVP-5120', defaults=dict(nombre='Dra. Lucía Paredes', especialidad='Dermatología'))

# Insumos con stock suficiente para los consumos de prueba.
jer, _ = Insumo.objects.get_or_create(nombre='Jeringa 5ml', defaults=dict(unidad='unidad', stock=100))
ant, _ = Insumo.objects.get_or_create(nombre='Antibiótico inyectable', defaults=dict(unidad='ampolla', stock=30))
gas, _ = Insumo.objects.get_or_create(nombre='Gasa estéril', defaults=dict(unidad='paquete', stock=45))
vac, _ = Insumo.objects.get_or_create(nombre='Vacuna antirrábica', defaults=dict(unidad='dosis', stock=25))

# Citas (minimo 5) con estados variados.
nuevas = [
    ('Luna', 'Pedro Díaz', 'Vacunación', date(2026, 10, 20), time(9, 30), 'Pendiente', v2),
    ('Toby', 'Marta Gil', 'Consulta', date(2026, 10, 21), time(11, 0), 'Confirmada', v3),
    ('Nala', 'Jorge Rojas', 'Baño', date(2026, 10, 9), time(15, 0), 'Atendida', v3),
]
for m, d, s, f, h, e, v in nuevas:
    Cita.objects.get_or_create(
        mascota=m, defaults=dict(dueno=d, servicio=s, fecha=f, hora=h, estado=e, veterinario=v))

c1, c2, c3, c4, c5 = list(Cita.objects.order_by('id')[:5])
Cita.objects.filter(pk=c1.pk, veterinario__isnull=True).update(veterinario=v1)
Cita.objects.filter(pk=c2.pk, veterinario__isnull=True).update(veterinario=v2)

# Consumos (minimo 8). Se agregan hasta completar 8 sin repetir los ya cargados.
consumos = [
    (c1, jer, 2, '1.50'), (c1, ant, 1, '18.00'), (c1, gas, 3, '2.50'),
    (c2, jer, 1, '1.50'), (c3, vac, 1, '35.00'), (c3, jer, 1, '1.50'),
    (c4, ant, 2, '18.00'), (c5, gas, 2, '2.50'),
]
for cita, insumo, cantidad, precio in consumos:
    if ConsumoInsumo.objects.count() >= 8:
        break
    ConsumoInsumo.objects.get_or_create(
        cita=cita, insumo=insumo, defaults=dict(cantidad=cantidad, precio_unitario=precio))

print('Citas:', Cita.objects.count(), '| Veterinarios:', Veterinario.objects.count(),
      '| Insumos:', Insumo.objects.count(), '| Consumos:', ConsumoInsumo.objects.count())
