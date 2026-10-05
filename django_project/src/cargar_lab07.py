from datetime import date, time
from vet.models import Cita, Veterinario, Insumo, ConsumoInsumo

v1 = Veterinario.objects.get(colegiatura='CMVP-4821')
v2 = Veterinario.objects.get(colegiatura='CMVP-3907')
v3 = Veterinario.objects.get(colegiatura='CMVP-5120')
jer = Insumo.objects.get(nombre='Jeringa 5ml')
ant = Insumo.objects.get(nombre='Antibiótico inyectable')
gas = Insumo.objects.get(nombres='Gasa estéril')
vac = Insumo.objects.get(nombre='Vacuna antirrábica')

c1, c2 = list(Cita.objects.order_by('id')[:2])
c1.veterinario = v1
c1.save()
c2.veterinario = v2
c2.save()

nuevas = [
    ('Luna', 'Pedro Díaz', 'Vacunación', date(2026, 10, 6), time(9, 30), 'Pendiente', v2),
    ('Toby', 'Marta Gil', 'Consulta', date(2026, 10, 7), time(11, 0), 'Confirmada', v3),
    ('Nala', 'Jorge Rojas', 'Baño', date(2026, 10, 8), time(15, 0), 'Atendida', v3),
]
for m, d, s, f, h, e, v in nuevas:
    Cita.objects.get_or_create(mascota=m, defaults=dict(dueno=d, servicio=s, fecha=f, hora=h, estado=e, veterinario=v))

c3, c4, c5 = list(Cita.objects.order_by('id'))[2:5]

if ConsumoInsumo.objects.count() == 0:
    ConsumoInsumo.objects.create(cita=c1, insumo=jer, cantidad=2, precio_unitario='1.50')
    ConsumoInsumo.objects.create(cita=c1, insumo=ant, cantidad=1, precio_unitario='18.00')
    ConsumoInsumo.objects.create(cita=c1, insumo=gas, cantidad=3, precio_unitario='2.50')
    ConsumoInsumo.objects.create(cita=c2, insumo=jer, cantidad=1, precio_unitario='1.50')
    ConsumoInsumo.objects.create(cita=c3, insumo=vac, cantidad=1, precio_unitario='35.00')
    ConsumoInsumo.objects.create(cita=c3, insumo=jer, cantidad=1, precio_unitario='1.50')
    ConsumoInsumo.objects.create(cita=c4, insumo=ant, cantidad=2, precio_unitario='18.00')
    ConsumoInsumo.objects.create(cita=c5, insumo=gas, cantidad=2, precio_unitario='2.50')

print(Cita.objects.count(), Veterinario.objects.count(), ConsumoInsumo.objects.count(), Insumo.objects.count())