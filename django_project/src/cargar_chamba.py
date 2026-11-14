# cargar_chamba.py
# Carga los prestadores de ejemplo de Chamba PE (los mismos del panel con datos a mano).
# Uso: python manage.py shell < cargar_chamba.py

from chamba.models import Prestador

Prestador.objects.all().delete()
Prestador.objects.bulk_create([
    Prestador(nombres='Carlos', apellidos='Ramos Quispe', rubro='Gasfitería', tarifa='60.00', estado='Aprobado'),
    Prestador(nombres='María', apellidos='Torres Vega', rubro='Costura', tarifa='25.00', estado='Pendiente'),
    Prestador(nombres='Luis', apellidos='Gamarra Soto', rubro='Electricidad', tarifa='50.00', estado='Aprobado'),
    Prestador(nombres='Ana', apellidos='Paredes Ríos', rubro='Primeros auxilios', tarifa='40.00', estado='Pendiente'),
    Prestador(nombres='Jorge', apellidos='Medina Salas', rubro='Carpintería', tarifa='70.00', estado='Suspendido'),
    Prestador(nombres='Rosa', apellidos='Díaz Huamán', rubro='Electricidad', tarifa='55.00', estado='Aprobado'),
])
print('Prestadores cargados:', Prestador.objects.count())
