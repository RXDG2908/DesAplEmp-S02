# ==================================================================
# ARCHIVO  : cargar_chamba.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : SCRIPT DE DATOS DE PRUEBA.
# ------------------------------------------------------------------
# LAB 12 - EJ 9: CARGA los 6 PRESTADORES de ejemplo (los mismos que el panel
#                del Lab 11 tenía escritos a mano).
# NOTA     : BORRA los prestadores existentes antes de cargar (no duplica).
# ------------------------------------------------------------------
# USO      : python manage.py shell < cargar_chamba.py
# ==================================================================

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
